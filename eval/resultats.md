# Résultats de l'évaluation

**10 / 10 réponses justes** (modèle `gemini-flash-lite-latest`, 08/11/2026).

| # | Question | Attendu | Résultat | Durée |
|---|---|---:|:---:|---:|
| Q1 | Quel est le chiffre d'affaires total de 2025 ? | 33 783 042,84 | ✅ | 21 s |
| Q2 | Combien de commandes ont été passées en 2025, tous statuts confondus ? | 19 845,00 | ✅ | 18 s |
| Q3 | Combien de clients différents ont passé au moins une commande en 2025 ? | 4 889,00 | ✅ | 39 s |
| Q4 | Quel est le panier moyen par commande en 2025 ? | 1 834,14 | ✅ | 8 s |
| Q5 | Quel est le chiffre d'affaires de décembre 2025 ? | 2 962 774,32 | ✅ | 394 s |
| Q6 | Quelle part des commandes de 2025 a été annulée, en pourcentage ? | 7,19 | ✅ | 18 s |
| Q7 | Quel est le chiffre d'affaires 2025 du produit qui a le plus rapporté cette année-là ? | 51 814,35 | ✅ | 18 s |
| Q8 | Quel pays a généré le plus gros chiffre d'affaires en 2025, et combien ? | 270 698,64 | ✅ | 18 s |
| Q9 | Quelle catégorie de produits a le plus rapporté en 2025, et combien ? | 4 007 567,54 | ✅ | 18 s |
| Q10 | Quelle est la quantité totale d'articles vendus le week-end en 2025, hors commandes annulées ? | 39 537,00 | ✅ | 15 s |

## Détail

### Q1 — Quel est le chiffre d'affaires total de 2025 ?

Attendu : `33783042.84` — juste

SQL de référence :
```sql
select sum(line_amount) from `portfolio-data-vr.marts.fct_sales` where order_day between '2025-01-01' and '2025-12-31' and status != 'cancelled'
```

SQL de l'agent :
```sql
SELECT
  SUM(line_amount) AS chiffre_affaires_2025
FROM
  `portfolio-data-vr.marts.fct_sales`
WHERE
  order_day >= '2025-01-01'
  AND order_day <= '2025-12-31'
  AND status != 'cancelled'

```

Réponse de l'agent :

> Le chiffre d'affaires total de l'année 2025 (hors commandes annulées) s'élève à **33 783 042,84 €**.
> 
> ### Requête SQL utilisée :
> ```sql
> SELECT
>   SUM(line_amount) AS chiffre_affaires_2025
> FROM
>   `portfolio-data-vr.marts.fct_sales`
> WHERE
>   order_day >= '2025-01-01'
>   AND order_day <= '2025-12-31'
>   AND status != 'cancelled'
> ```
> 
> ### Interprétation :
> Ce montant représente la somme totale des lignes de ventes effectives pour l'année 2025, en excluant les commandes dont le statut est « cancelled », conformément aux règles de gestion du chiffre d'affaires.

### Q2 — Combien de commandes ont été passées en 2025, tous statuts confondus ?

Attendu : `19845.00` — juste

SQL de référence :
```sql
select count(distinct order_id) from `portfolio-data-vr.marts.fct_sales` where order_day between '2025-01-01' and '2025-12-31'
```

SQL de l'agent :
```sql
SELECT COUNT(DISTINCT order_id) AS total_orders
FROM `portfolio-data-vr.marts.fct_sales`
WHERE order_day >= '2025-01-01' AND order_day <= '2025-12-31'

```

Réponse de l'agent :

> En 2025, **19 845** commandes ont été passées (tous statuts confondus, y compris les commandes annulées, conformément à la règle de comptage des commandes).
> 
> ### SQL utilisé :
> ```sql
> SELECT COUNT(DISTINCT order_id) AS total_orders
> FROM `portfolio-data-vr.marts.fct_sales`
> WHERE order_day >= '2025-01-01' AND order_day <= '2025-12-31'
> ```
> 
> ### Interprétation :
> Ce chiffre représente l'ensemble de l'activité commerciale enregistrée sur l'année 2025, avant éventuel retrait des commandes annulées (qui dépend de l'analyse menée, par exemple sur le chiffre d'affaires).

### Q3 — Combien de clients différents ont passé au moins une commande en 2025 ?

Attendu : `4889.00` — juste

SQL de référence :
```sql
select count(distinct customer_key) from `portfolio-data-vr.marts.fct_sales` where order_day between '2025-01-01' and '2025-12-31'
```

SQL de l'agent :
```sql
SELECT COUNT(DISTINCT customer_key) AS nb_clients
FROM `portfolio-data-vr.marts.fct_sales`
WHERE order_day BETWEEN '2025-01-01' AND '2025-12-31'

```

Réponse de l'agent :

> **Chiffres :**
> En 2025, **4 889** clients différents ont passé au moins une commande.
> 
> **Requête SQL utilisée :**
> ```sql
> SELECT COUNT(DISTINCT customer_key) AS nb_clients
> FROM `portfolio-data-vr.marts.fct_sales`
> WHERE order_day BETWEEN '2025-01-01' AND '2025-12-31'
> ```
> 
> **Interprétation :**
> Ce chiffre représente la base active de clients ayant initié au moins une commande sur l'année 2025 (conformément à la règle qui inclut tous les statuts, y compris les commandes annulées, pour le décompte des commandes ou des clients).

### Q4 — Quel est le panier moyen par commande en 2025 ?

Attendu : `1834.14` — juste

SQL de référence :
```sql
select sum(line_amount) / count(distinct order_id) from `portfolio-data-vr.marts.fct_sales` where order_day between '2025-01-01' and '2025-12-31' and status != 'cancelled'
```

SQL de l'agent :
```sql
SELECT
  ROUND(SUM(line_amount) / COUNT(DISTINCT order_id), 2) AS panier_moyen
FROM
  `portfolio-data-vr.marts.fct_sales`
WHERE
  order_day >= '2025-01-01'
  AND order_day < '2026-01-01'
  AND status != 'cancelled';

```

Réponse de l'agent :

> Pour répondre à votre question, voici l'analyse du panier moyen en 2025 (en excluant les commandes annulées).
> 
> ### **Chiffre**
> * **Panier moyen en 2025 :** **1 834,14 €**
> 
> ### **Requête SQL utilisée**
> ```sql
> SELECT
>   ROUND(SUM(line_amount) / COUNT(DISTINCT order_id), 2) AS panier_moyen
> FROM
>   `portfolio-data-vr.marts.fct_sales`
> WHERE
>   order_day >= '2025-01-01'
>   AND order_day < '2026-01-01'
>   AND status != 'cancelled';
> ```
> 
> ### **Interprétation**
> En 2025, chaque commande validée (hors statuts annulés) génère en moyenne un montant de **1 834,14 €**.

### Q5 — Quel est le chiffre d'affaires de décembre 2025 ?

Attendu : `2962774.32` — juste

SQL de référence :
```sql
select sum(line_amount) from `portfolio-data-vr.marts.fct_sales` where order_day between '2025-12-01' and '2025-12-31' and status != 'cancelled'
```

SQL de l'agent :
```sql
SELECT
  SUM(line_amount) AS chiffre_affaires
FROM
  `portfolio-data-vr.marts.fct_sales`
WHERE
  order_day >= '2025-12-01'
  AND order_day <= '2025-12-31'
  AND status != 'cancelled'

```

Réponse de l'agent :

> **Chiffre d'affaires de décembre 2025 :** 2 962 774,32 €
> 
> **Requête SQL utilisée :**
> ```sql
> SELECT
>   SUM(line_amount) AS chiffre_affaires
> FROM
>   `portfolio-data-vr.marts.fct_sales`
> WHERE
>   order_day >= '2025-12-01'
>   AND order_day <= '2025-12-31'
>   AND status != 'cancelled'
> ```
> 
> **Interprétation :**
> Le chiffre d'affaires total généré par les ventes validées (hors commandes annulées) pour le mois de décembre 2025 s'élève à 2 962 774,32 €.

### Q6 — Quelle part des commandes de 2025 a été annulée, en pourcentage ?

Attendu : `7.19` — juste

SQL de référence :
```sql
select 100 * count(distinct if(status = 'cancelled', order_id, null)) / count(distinct order_id) from `portfolio-data-vr.marts.fct_sales` where order_day between '2025-01-01' and '2025-12-31'
```

SQL de l'agent :
```sql
SELECT 
  COUNT(DISTINCT order_id) AS total_commandes,
  COUNT(DISTINCT CASE WHEN status = 'cancelled' THEN order_id END) AS commandes_annulees,
  SAFE_DIVIDE(
    COUNT(DISTINCT CASE WHEN status = 'cancelled' THEN order_id END),
    COUNT(DISTINCT order_id)
  ) * 100 AS pourcentage_annulees
FROM `portfolio-data-vr.marts.fct_sales`
WHERE order_day >= '2025-01-01' AND order_day <= '2025-12-31'

```

Réponse de l'agent :

> **SQL utilisé :**
> ```sql
> SELECT 
>   COUNT(DISTINCT order_id) AS total_commandes,
>   COUNT(DISTINCT CASE WHEN status = 'cancelled' THEN order_id END) AS commandes_annulees,
>   SAFE_DIVIDE(
>     COUNT(DISTINCT CASE WHEN status = 'cancelled' THEN order_id END),
>     COUNT(DISTINCT order_id)
>   ) * 100 AS pourcentage_annulees
> FROM `portfolio-data-vr.marts.fct_sales`
> WHERE order_day >= '2025-01-01' AND order_day <= '2025-12-31'
> ```
> 
> **Chiffres :**
> - **Total des commandes en 2025 :** 19 845
> - **Commandes annulées :** 1 426
> - **Part des commandes annulées :** **7,19 %**
> 
> **Interprétation :**
> En 2025, un peu plus de 7 % des commandes passées ont été annulées, ce qui représente 1 426 commandes sur un total de 19 845.

### Q7 — Quel est le chiffre d'affaires 2025 du produit qui a le plus rapporté cette année-là ?

Attendu : `51814.35` — juste

SQL de référence :
```sql
select sum(line_amount) ca from `portfolio-data-vr.marts.fct_sales` where order_day between '2025-01-01' and '2025-12-31' and status != 'cancelled' group by product_key order by ca desc limit 1
```

SQL de l'agent :
```sql
SELECT 
    p.product_name,
    p.sku,
    SUM(f.line_amount) AS chiffre_affaires
FROM `portfolio-data-vr.marts.fct_sales` f
JOIN `portfolio-data-vr.marts.dim_product` p ON f.product_key = p.product_key
WHERE f.order_day BETWEEN '2025-01-01' AND '2025-12-31'
  AND f.status != 'cancelled'
GROUP BY p.product_name, p.sku
ORDER BY chiffre_affaires DESC
LIMIT 1

```

Réponse de l'agent :

> **Chiffre d'affaires :** 51 814,35 € (pour le produit *Balanced global migration*, SKU : `SKU-000936`).
> 
> **Requête SQL utilisée :**
> ```sql
> SELECT 
>     p.product_name,
>     p.sku,
>     SUM(f.line_amount) AS chiffre_affaires
> FROM `portfolio-data-vr.marts.fct_sales` f
> JOIN `portfolio-data-vr.marts.dim_product` p ON f.product_key = p.product_key
> WHERE f.order_day BETWEEN '2025-01-01' AND '2025-12-31'
>   AND f.status != 'cancelled'
> GROUP BY p.product_name, p.sku
> ORDER BY chiffre_affaires DESC
> LIMIT 1
> ```
> 
> **Interprétation :** 
> En 2025 (hors commandes annulées), le produit le plus performant en termes de chiffre d'affaires est *Balanced global migration*, qui a généré 51 814,35 € de ventes.

### Q8 — Quel pays a généré le plus gros chiffre d'affaires en 2025, et combien ?

Attendu : `270698.64` — juste

SQL de référence :
```sql
select sum(f.line_amount) ca from `portfolio-data-vr.marts.fct_sales` f join `portfolio-data-vr.marts.dim_customer` c using (customer_key) where f.order_day between '2025-01-01' and '2025-12-31' and f.status != 'cancelled' group by c.country_name order by ca desc limit 1
```

SQL de l'agent :
```sql
SELECT 
  c.country_name,
  SUM(s.line_amount) AS total_revenue
FROM `portfolio-data-vr.marts.fct_sales` s
JOIN `portfolio-data-vr.marts.dim_customer` c
  ON s.customer_key = c.customer_key
WHERE s.order_day >= '2025-01-01' 
  AND s.order_day < '2026-01-01'
  AND s.status != 'cancelled'
GROUP BY c.country_name
ORDER BY total_revenue DESC
LIMIT 1

```

Réponse de l'agent :

> **Requête SQL utilisée :**
> ```sql
> SELECT 
>   c.country_name,
>   SUM(s.line_amount) AS total_revenue
> FROM `portfolio-data-vr.marts.fct_sales` s
> JOIN `portfolio-data-vr.marts.dim_customer` c
>   ON s.customer_key = c.customer_key
> WHERE s.order_day >= '2025-01-01' 
>   AND s.order_day < '2026-01-01'
>   AND s.status != 'cancelled'
> GROUP BY c.country_name
> ORDER BY total_revenue DESC
> LIMIT 1
> ```
> 
> **Résultats :**
> - **Pays :** Chine
> - **Chiffre d'affaires (hors commandes annulées) :** 270 698,64 €
> 
> **Interprétation :**
> En 2025, la Chine est le pays qui a généré le chiffre d'affaires le plus élevé parmi l'ensemble des clients, atteignant un total de 270 698,64 € (en excluant les commandes annulées conformément aux règles de calcul du chiffre d'affaires).

### Q9 — Quelle catégorie de produits a le plus rapporté en 2025, et combien ?

Attendu : `4007567.54` — juste

SQL de référence :
```sql
select sum(f.line_amount) ca from `portfolio-data-vr.marts.fct_sales` f join `portfolio-data-vr.marts.dim_product` p using (product_key) where f.order_day between '2025-01-01' and '2025-12-31' and f.status != 'cancelled' group by p.category order by ca desc limit 1
```

SQL de l'agent :
```sql
SELECT 
    p.category, 
    SUM(s.line_amount) AS total_revenue
FROM 
    `portfolio-data-vr.marts.fct_sales` s
JOIN 
    `portfolio-data-vr.marts.dim_product` p ON s.product_key = p.product_key
WHERE 
    s.order_day >= '2025-01-01' 
    AND s.order_day < '2026-01-01'
    AND s.status != 'cancelled'
GROUP BY 
    p.category
ORDER BY 
    total_revenue DESC
LIMIT 1;
```

Réponse de l'agent :

> En 2025, la catégorie de produits qui a le plus rapporté est **Jouets**, avec un chiffre d'affaires total de **4 007 567,54 €** (en excluant les commandes annulées).
> 
> ### Requête SQL utilisée :
> ```sql
> SELECT 
>     p.category, 
>     SUM(s.line_amount) AS total_revenue
> FROM 
>     `portfolio-data-vr.marts.fct_sales` s
> JOIN 
>     `portfolio-data-vr.marts.dim_product` p ON s.product_key = p.product_key
> WHERE 
>     s.order_day >= '2025-01-01' 
>     AND s.order_day < '2026-01-01'
>     AND s.status != 'cancelled'
> GROUP BY 
>     p.category
> ORDER BY 
>     total_revenue DESC
> LIMIT 1;
> ```
> 
> ### Interprétation :
> La catégorie "Jouets" domine les ventes sur l'année 2025, confirmant son rôle de premier contributeur au chiffre d'affaires global de l'entreprise parmi l'ensemble des catégories de produits référencées.

### Q10 — Quelle est la quantité totale d'articles vendus le week-end en 2025, hors commandes annulées ?

Attendu : `39537.00` — juste

SQL de référence :
```sql
select sum(f.quantity) from `portfolio-data-vr.marts.fct_sales` f join `portfolio-data-vr.marts.dim_date` d using (date_key) where d.est_weekend and f.order_day between '2025-01-01' and '2025-12-31' and f.status != 'cancelled'
```

SQL de l'agent :
```sql
SELECT
  SUM(s.quantity) AS total_articles_weekend_2025
FROM
  `portfolio-data-vr.marts.fct_sales` AS s
JOIN
  `portfolio-data-vr.marts.dim_date` AS d
  ON s.order_day = d.date
WHERE
  d.annee = 2025
  AND d.est_weekend = TRUE
  AND s.order_day >= '2025-01-01' AND s.order_day <= '2025-12-31'
  AND s.status != 'cancelled'

```

Réponse de l'agent :

> En 2025, la quantité totale d'articles vendus le week-end (hors commandes annulées) s'élève à **39 537**.
> 
> ### Requête SQL utilisée :
> ```sql
> SELECT
>   SUM(s.quantity) AS total_articles_weekend_2025
> FROM
>   `portfolio-data-vr.marts.fct_sales` AS s
> JOIN
>   `portfolio-data-vr.marts.dim_date` AS d
>   ON s.order_day = d.date
> WHERE
>   d.annee = 2025
>   AND d.est_weekend = TRUE
>   AND s.order_day >= '2025-01-01' AND s.order_day <= '2025-12-31'
>   AND s.status != 'cancelled'
> ```
> 
> ### Interprétation :
> Ce chiffre représente le nombre cumulé d'articles commandés les samedis et dimanches de l'année 2025, en excluant l'ensemble des lignes de ventes associées à un statut de commande annulé (`cancelled`), conformément aux règles de gestion.
