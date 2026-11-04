# Résultats de l'évaluation

**9 / 10 réponses justes** (modèle `gemini-flash-lite-latest`, 04/11/2026).

| # | Question | Attendu | Résultat | Durée |
|---|---|---:|:---:|---:|
| Q1 | Quel est le chiffre d'affaires total de 2025 ? | 33 783 042,84 | ✅ | 9 s |
| Q2 | Combien de commandes ont été passées en 2025, tous statuts confondus ? | 19 845,00 | ✅ | 9 s |
| Q3 | Combien de clients différents ont passé au moins une commande en 2025 ? | 4 889,00 | ❌ | 11 s |
| Q4 | Quel est le panier moyen par commande en 2025 ? | 1 834,14 | ✅ | 10 s |
| Q5 | Quel est le chiffre d'affaires de décembre 2025 ? | 2 962 774,32 | ✅ | 6 s |
| Q6 | Quelle part des commandes de 2025 a été annulée, en pourcentage ? | 7,19 | ✅ | 10 s |
| Q7 | Quel est le chiffre d'affaires 2025 du produit qui a le plus rapporté cette année-là ? | 51 814,35 | ✅ | 10 s |
| Q8 | Quel pays a généré le plus gros chiffre d'affaires en 2025, et combien ? | 270 698,64 | ✅ | 12 s |
| Q9 | Quelle catégorie de produits a le plus rapporté en 2025, et combien ? | 4 007 567,54 | ✅ | 11 s |
| Q10 | Quelle est la quantité totale d'articles vendus le week-end en 2025, hors commandes annulées ? | 39 537,00 | ✅ | 9 s |

## Détail

### Q1 — Quel est le chiffre d'affaires total de 2025 ?

Attendu : `33783042.84` — juste

SQL de référence :
```sql
select sum(line_amount) from `portfolio-data-vr.marts.fct_sales` where order_day between '2025-01-01' and '2025-12-31' and status != 'cancelled'
```

SQL de l'agent :
```sql
SELECT SUM(line_amount) AS total_revenue
FROM `portfolio-data-vr.marts.fct_sales`
WHERE order_day BETWEEN '2025-01-01' AND '2025-12-31'
  AND status != 'cancelled'

```

Réponse de l'agent :

> **Chiffre d'affaires total pour l'année 2025 :** 33 783 042,84 € (en excluant les commandes dont le statut est `'cancelled'`).
> 
> **Requête SQL utilisée :**
> ```sql
> SELECT SUM(line_amount) AS total_revenue
> FROM `portfolio-data-vr.marts.fct_sales`
> WHERE order_day BETWEEN '2025-01-01' AND '2025-12-31'
>   AND status != 'cancelled'
> ```
> 
> **Interprétation :**
> Ce montant représente la somme totale des ventes (montant de ligne) réalisées au cours de l'année 2025, après filtration des commandes annulées.

### Q2 — Combien de commandes ont été passées en 2025, tous statuts confondus ?

Attendu : `19845.00` — juste

SQL de référence :
```sql
select count(distinct order_id) from `portfolio-data-vr.marts.fct_sales` where order_day between '2025-01-01' and '2025-12-31'
```

SQL de l'agent :
```sql
SELECT COUNT(DISTINCT order_id) AS nb_commandes
FROM `portfolio-data-vr.marts.fct_sales`
WHERE order_day BETWEEN '2025-01-01' AND '2025-12-31'

```

Réponse de l'agent :

> En 2025, **19 845** commandes ont été passées, tous statuts confondus.
> 
> ### Requête SQL utilisée :
> ```sql
> SELECT COUNT(DISTINCT order_id) AS nb_commandes
> FROM `portfolio-data-vr.marts.fct_sales`
> WHERE order_day BETWEEN '2025-01-01' AND '2025-12-31'
> ```
> 
> ### Interprétation :
> Ce chiffre représente le nombre total de commandes uniques enregistrées dans la table des ventes (`fct_sales`) au cours de l'année 2025, en filtrant directement sur la colonne partitionnée `order_day` pour optimiser la requête, et ce sans exclure aucun statut (comme demandé).

### Q3 — Combien de clients différents ont passé au moins une commande en 2025 ?

Attendu : `4889.00` — faux

SQL de référence :
```sql
select count(distinct customer_key) from `portfolio-data-vr.marts.fct_sales` where order_day between '2025-01-01' and '2025-12-31'
```

SQL de l'agent :
```sql
SELECT 
  COUNT(DISTINCT customer_key) AS nb_customers
FROM `portfolio-data-vr.marts.fct_sales`
WHERE order_day >= '2025-01-01' 
  AND order_day < '2026-01-01'
  AND status != 'cancelled'

```

Réponse de l'agent :

> En 2025, **4 854** clients différents ont passé au moins une commande (en excluant les commandes annulées).
> 
> ### Requête SQL utilisée :
> ```sql
> SELECT 
>   COUNT(DISTINCT customer_key) AS nb_customers
> FROM `portfolio-data-vr.marts.fct_sales`
> WHERE order_day >= '2025-01-01' 
>   AND order_day < '2026-01-01'
>   AND status != 'cancelled'
> ```
> 
> ### Interprétation :
> Ce chiffre indique le nombre de clients distincts actifs sur l'année 2025, après avoir filtré les commandes dont le statut est `'cancelled'`.

### Q4 — Quel est le panier moyen par commande en 2025 ?

Attendu : `1834.14` — juste

SQL de référence :
```sql
select sum(line_amount) / count(distinct order_id) from `portfolio-data-vr.marts.fct_sales` where order_day between '2025-01-01' and '2025-12-31' and status != 'cancelled'
```

SQL de l'agent :
```sql
SELECT 
    AVG(order_total) AS panier_moyen
FROM (
    SELECT 
        order_id,
        SUM(line_amount) AS order_total
    FROM `portfolio-data-vr.marts.fct_sales`
    WHERE order_day >= '2025-01-01' 
      AND order_day <= '2025-12-31'
      AND status != 'cancelled'
    GROUP BY order_id
)

```

Réponse de l'agent :

> Pour répondre à votre question, voici l'analyse du panier moyen par commande en 2025 (en excluant les commandes annulées `status != 'cancelled'` et en filtrant sur la colonne partitionnée `order_day`) :
> 
> ### Chiffres
> * **Panier moyen par commande en 2025** : **1 834,14 €**
> 
> ### Requête SQL utilisée
> ```sql
> SELECT 
>     AVG(order_total) AS panier_moyen
> FROM (
>     SELECT 
>         order_id,
>         SUM(line_amount) AS order_total
>     FROM `portfolio-data-vr.marts.fct_sales`
>     WHERE order_day >= '2025-01-01' 
>       AND order_day <= '2025-12-31'
>       AND status != 'cancelled'
>     GROUP BY order_id
> )
> ```
> 
> ### Interprétation
> En 2025, le montant moyen dépensé par les clients pour une commande validée (hors statut `cancelled`) s'élève à environ **1 834,14 €**. Ce montant représente la valeur totale des lignes de commande cumulées par `order_id` pour l'année civile.

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

> Le chiffre d'affaires pour le mois de décembre 2025 s'élève à **2 962 774,32 €** (en excluant les commandes dont le statut est `cancelled`).
> 
> ### Requête SQL utilisée :
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
> ### Interprétation :
> Ce montant représente la valeur totale des lignes de commande validées (payées, expédiées, livrées ou en attente) enregistrées durant le mois de décembre 2025.

### Q6 — Quelle part des commandes de 2025 a été annulée, en pourcentage ?

Attendu : `7.19` — juste

SQL de référence :
```sql
select 100 * count(distinct if(status = 'cancelled', order_id, null)) / count(distinct order_id) from `portfolio-data-vr.marts.fct_sales` where order_day between '2025-01-01' and '2025-12-31'
```

SQL de l'agent :
```sql
SELECT
  COUNT(DISTINCT order_id) AS total_orders,
  COUNT(DISTINCT CASE WHEN status = 'cancelled' THEN order_id END) AS cancelled_orders,
  ROUND(100.0 * COUNT(DISTINCT CASE WHEN status = 'cancelled' THEN order_id END) / COUNT(DISTINCT order_id), 2) AS cancelled_percentage
FROM `portfolio-data-vr.marts.fct_sales`
WHERE order_day BETWEEN '2025-01-01' AND '2025-12-31'

```

Réponse de l'agent :

> En 2025, sur un total de 19 845 commandes, 1 426 ont été annulées, soit une part de **7,19 %**.
> 
> ### Requête SQL utilisée :
> ```sql
> SELECT
>   COUNT(DISTINCT order_id) AS total_orders,
>   COUNT(DISTINCT CASE WHEN status = 'cancelled' THEN order_id END) AS cancelled_orders,
>   ROUND(100.0 * COUNT(DISTINCT CASE WHEN status = 'cancelled' THEN order_id END) / COUNT(DISTINCT order_id), 2) AS cancelled_percentage
> FROM `portfolio-data-vr.marts.fct_sales`
> WHERE order_day BETWEEN '2025-01-01' AND '2025-12-31'
> ```
> 
> ### Interprétation :
> Près de 7,2 % des commandes passées en 2025 ont connu une annulation (statut `cancelled`), ce qui représente un taux d'annulation à surveiller pour évaluer la satisfaction client ou les problèmes de stock et de paiement.

### Q7 — Quel est le chiffre d'affaires 2025 du produit qui a le plus rapporté cette année-là ?

Attendu : `51814.35` — juste

SQL de référence :
```sql
select sum(line_amount) ca from `portfolio-data-vr.marts.fct_sales` where order_day between '2025-01-01' and '2025-12-31' and status != 'cancelled' group by product_key order by ca desc limit 1
```

SQL de l'agent :
```sql
SELECT 
    p.product_key,
    p.product_name,
    SUM(f.line_amount) AS chiffre_affaires
FROM `portfolio-data-vr.marts.fct_sales` f
JOIN `portfolio-data-vr.marts.dim_product` p ON f.product_key = p.product_key
WHERE f.order_day >= '2025-01-01' 
  AND f.order_day < '2026-01-01'
  AND f.status != 'cancelled'
GROUP BY 1, 2
ORDER BY chiffre_affaires DESC
LIMIT 1;
```

Réponse de l'agent :

> En 2025 (hors commandes annulées), le produit qui a généré le chiffre d'affaires le plus élevé est **"Balanced global migration"** (clé produit : 937), avec un chiffre d'affaires de **51 814,35 €**.
> 
> ### Requête SQL utilisée :
> ```sql
> SELECT 
>     p.product_key,
>     p.product_name,
>     SUM(f.line_amount) AS chiffre_affaires
> FROM `portfolio-data-vr.marts.fct_sales` f
> JOIN `portfolio-data-vr.marts.dim_product` p ON f.product_key = p.product_key
> WHERE f.order_day >= '2025-01-01' 
>   AND f.order_day < '2026-01-01'
>   AND f.status != 'cancelled'
> GROUP BY 1, 2
> ORDER BY chiffre_affaires DESC
> LIMIT 1;
> ```
> 
> ### Interprétation :
> Ce produit s'est imposé comme le meilleur contributeur aux ventes de l'année 2025, devançant l'ensemble des autres références du catalogue sur la période.

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
FROM
  `portfolio-data-vr.marts.fct_sales` AS s
JOIN
  `portfolio-data-vr.marts.dim_customer` AS c
  ON s.customer_key = c.customer_key
WHERE
  s.order_day >= '2025-01-01'
  AND s.order_day < '2026-01-01'
  AND s.status != 'cancelled'
GROUP BY
  c.country_name
ORDER BY
  total_revenue DESC
LIMIT 1;
```

Réponse de l'agent :

> En 2025 (hors commandes annulées), le pays ayant généré le plus grand chiffre d'affaires est la **Chine** avec un total de **270 698,64**.
> 
> ### Requête SQL utilisée :
> ```sql
> SELECT
>   c.country_name,
>   SUM(s.line_amount) AS total_revenue
> FROM
>   `portfolio-data-vr.marts.fct_sales` AS s
> JOIN
>   `portfolio-data-vr.marts.dim_customer` AS c
>   ON s.customer_key = c.customer_key
> WHERE
>   s.order_day >= '2025-01-01'
>   AND s.order_day < '2026-01-01'
>   AND s.status != 'cancelled'
> GROUP BY
>   c.country_name
> ORDER BY
>   total_revenue DESC
> LIMIT 1;
> ```
> 
> ### Interprétation :
> Ce résultat montre que la Chine se positionne comme le marché le plus contributeur en termes de ventes pour l'année 2025 parmi l'ensemble des clients enregistrés dans la dimension client (`dim_customer`).

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
FROM `portfolio-data-vr.marts.fct_sales` s
JOIN `portfolio-data-vr.marts.dim_product` p
  ON s.product_key = p.product_key
WHERE s.order_day >= '2025-01-01' 
  AND s.order_day < '2026-01-01'
  AND s.status != 'cancelled'
GROUP BY p.category
ORDER BY total_revenue DESC
LIMIT 1;
```

Réponse de l'agent :

> En 2025, la catégorie de produits qui a le plus rapporté est **Jouets**, avec un chiffre d'affaires total de **4 007 567,54 €** (après exclusion des commandes dont le statut est `'cancelled'`).
> 
> ### Requête SQL utilisée :
> ```sql
> SELECT 
>   p.category,
>   SUM(s.line_amount) AS total_revenue
> FROM `portfolio-data-vr.marts.fct_sales` s
> JOIN `portfolio-data-vr.marts.dim_product` p
>   ON s.product_key = p.product_key
> WHERE s.order_day >= '2025-01-01' 
>   AND s.order_day < '2026-01-01'
>   AND s.status != 'cancelled'
> GROUP BY p.category
> ORDER BY total_revenue DESC
> LIMIT 1;
> ```
> 
> ### Interprétation :
> La catégorie **Jouets** se positionne en tête des ventes pour l'année 2025, confirmant son poids majeur dans l'activité commerciale sur cette période.

### Q10 — Quelle est la quantité totale d'articles vendus le week-end en 2025, hors commandes annulées ?

Attendu : `39537.00` — juste

SQL de référence :
```sql
select sum(f.quantity) from `portfolio-data-vr.marts.fct_sales` f join `portfolio-data-vr.marts.dim_date` d using (date_key) where d.est_weekend and f.order_day between '2025-01-01' and '2025-12-31' and f.status != 'cancelled'
```

SQL de l'agent :
```sql
SELECT
  SUM(f.quantity) AS total_articles_vendus
FROM
  `portfolio-data-vr.marts.fct_sales` f
JOIN
  `portfolio-data-vr.marts.dim_date` d
ON
  f.date_key = d.date_key
WHERE
  f.order_day BETWEEN '2025-01-01' AND '2025-12-31'
  AND d.est_weekend = TRUE
  AND f.status != 'cancelled'

```

Réponse de l'agent :

> La quantité totale d'articles vendus le week-end en 2025 (hors commandes annulées) est de **39 537** articles.
> 
> ### Requête SQL utilisée :
> ```sql
> SELECT
>   SUM(f.quantity) AS total_articles_vendus
> FROM
>   `portfolio-data-vr.marts.fct_sales` f
> JOIN
>   `portfolio-data-vr.marts.dim_date` d
> ON
>   f.date_key = d.date_key
> WHERE
>   f.order_day BETWEEN '2025-01-01' AND '2025-12-31'
>   AND d.est_weekend = TRUE
>   AND f.status != 'cancelled'
> ```
> 
> ### Interprétation :
> Ce chiffre représente le volume total d'articles commandés au cours de l'année 2025 pendant les samedis et dimanches (en s'appuyant sur le filtre de partitionnement `order_day` et la table de dimension temps `dim_date`), après avoir exclu les commandes dont le statut est `cancelled`.
