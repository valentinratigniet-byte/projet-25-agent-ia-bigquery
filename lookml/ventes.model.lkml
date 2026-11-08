connection: "bigquery_portfolio"
include: "/views/*.view.lkml"

explore: fct_sales {
  label: "Ventes"
  description: "Lignes de vente 2023-2025 (schéma en étoile du projet 13)."
  # fct_sales est partitionnée par jour : on force un filtre de date, modifiable, pour ne pas lire toute la table
  always_filter: {
    filters: [fct_sales.commande_date: "2025"]
  }

  join: dim_customer {
    type: left_outer
    relationship: many_to_one
    sql_on: ${fct_sales.customer_key} = ${dim_customer.customer_key} ;;
  }
  join: dim_product {
    type: left_outer
    relationship: many_to_one
    sql_on: ${fct_sales.product_key} = ${dim_product.product_key} ;;
  }
  join: dim_date {
    type: left_outer
    relationship: many_to_one
    sql_on: ${fct_sales.date_key} = ${dim_date.date_key} ;;
  }
}
