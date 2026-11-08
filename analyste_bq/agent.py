"""Analyste BigQuery : agent ADK en lecture seule sur portfolio-data-vr.marts (projet 13)."""
import os

from google.adk.agents import Agent
from google.adk.integrations.bigquery import BigQueryCredentialsConfig, BigQueryToolset
from google.adk.integrations.bigquery.config import BigQueryToolConfig, WriteMode
import google.auth

credentials, _ = google.auth.default()  # gcloud auth application-default login

bigquery = BigQueryToolset(
    credentials_config=BigQueryCredentialsConfig(credentials=credentials),
    bigquery_tool_config=BigQueryToolConfig(
        write_mode=WriteMode.BLOCKED,          # SELECT uniquement
        maximum_bytes_billed=1_000_000_000,     # garde-fou : 1 Go max par requête
        compute_project_id="portfolio-data-vr",
        location="EU",
    ),
    # pas de forecast / ask_data_insights : appels ML ou API potentiellement facturés
    tool_filter=["list_dataset_ids", "get_dataset_info", "list_table_ids",
                 "get_table_info", "execute_sql"],
)

root_agent = Agent(
    name="analyste_bq",
    model=os.getenv("MODEL", "gemini-flash-lite-latest"),
    description="Répond en français aux questions sur l'entrepôt des ventes.",
    instruction=(
        "Tu es un analyste data. Tu réponds en français aux questions sur le dataset "
        "BigQuery `portfolio-data-vr.marts` (schéma en étoile : fct_sales, dim_customer, "
        "dim_product, dim_date). Commence par lire le schéma des tables utiles, écris un "
        "SQL GoogleSQL simple, exécute-le, puis réponds avec les chiffres, le SQL utilisé "
        "et une phrase d'interprétation. Filtre sur order_day quand c'est possible "
        "(table partitionnée). Statuts : paid, shipped, delivered, pending, cancelled. "
        "Règle des annulées, à appliquer seulement là où elle vaut : pour un montant (chiffre d'affaires, "
        "panier moyen) ou une quantité vendue, exclus status = 'cancelled' et précise-le. Pour compter des "
        "commandes ou des clients, garde tous les statuts (une commande annulée a bien été passée), sauf si la "
        "question demande d'exclure les annulées. Tu ne modifies jamais de données. Si la question sort du "
        "périmètre des données, dis-le."
    ),
    tools=[bigquery],
)
