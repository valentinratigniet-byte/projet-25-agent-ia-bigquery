"""Contrôle de la couche LookML sans instance Looker (payante) :
1. chaque fichier .lkml doit être analysable (parseur lkml) ;
2. les mesures de fct_sales sont compilées en SQL, exécutées sur BigQuery pour 2025 et comparées aux valeurs de
   référence de eval/questions.json : la couche sémantique doit donner les mêmes chiffres que l'évaluation.
Usage : python lookml/verifier.py
"""
import json, re
from pathlib import Path

import lkml
from google.cloud import bigquery

ICI = Path(__file__).resolve().parent
REF = ICI.parent / "eval" / "questions.json"
# mesure LookML -> question de l'évaluation dont le SQL de référence donne la même valeur
ATTENDUS = {"chiffre_affaires": "Q1", "nb_commandes": "Q2", "nb_clients": "Q3", "panier_moyen": "Q4"}

fichiers = {p.name: lkml.load(p.read_text(encoding="utf-8")) for p in ICI.rglob("*.lkml")}
vue = fichiers["fct_sales.view.lkml"]["views"][0]
dims = {d["name"]: d["sql"].strip(" ;") for d in vue["dimensions"]}
mesures = {m["name"]: m for m in vue["measures"]}
REF_CHAMP = re.compile(r"\$\{(\w+)\}")


def sql_dim(expr):
    expr = expr.replace("${TABLE}", "f")
    return REF_CHAMP.sub(lambda m: f"({sql_dim(dims[m.group(1)])})", expr)


def sql_mesure(nom):
    m = mesures[nom]
    if m["type"] == "number":
        return REF_CHAMP.sub(lambda r: f"({sql_mesure(r.group(1))})", m["sql"].strip(" ;"))
    x = sql_dim(m["sql"].strip(" ;"))
    # lkml range « filters: [champ: "valeur"] » sous filters__all, liste de listes de {champ: valeur}
    for f in sum(m.get("filters__all", []), []):  # ponytail: seuls les filtres yesno sont gérés, assez pour cette vue
        (champ, valeur), = f.items()
        cond = sql_dim(dims[champ])
        x = f"IF({cond if valeur == 'yes' else f'NOT ({cond})'}, {x}, NULL)"
    return {"sum": f"SUM({x})", "count_distinct": f"COUNT(DISTINCT {x})"}[m["type"]]


def main():
    print(f"{len(fichiers)} fichiers LookML analysés, {len(mesures)} mesures dans fct_sales")
    refs = {q["id"]: q["sql"] for q in json.loads(REF.read_text(encoding="utf-8"))}
    bq = bigquery.Client(project="portfolio-data-vr", location="EU")
    cols = ", ".join(f"{sql_mesure(n)} AS {n}" for n in ATTENDUS)
    obtenu = dict(list(bq.query(f"SELECT {cols} FROM `portfolio-data-vr.marts.fct_sales` f "
                                "WHERE f.order_day BETWEEN '2025-01-01' AND '2025-12-31'").result())[0])
    ko = 0
    for nom, q in ATTENDUS.items():
        attendu = float(list(bq.query(refs[q]).result())[0][0])
        ok = abs(float(obtenu[nom]) - attendu) < 0.01
        ko += not ok
        print(f"{'OK ' if ok else 'KO '} {nom:<18} LookML {float(obtenu[nom]):>16,.2f}   référence {q} {attendu:>16,.2f}")
    assert ko == 0, f"{ko} mesure(s) divergent de la référence"


if __name__ == "__main__":
    main()
