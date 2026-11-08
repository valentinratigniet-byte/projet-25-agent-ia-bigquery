view: dim_product {
  sql_table_name: `portfolio-data-vr.marts.dim_product` ;;
  label: "Produit"

  dimension: product_key { primary_key: yes hidden: yes type: number sql: ${TABLE}.product_key ;; }
  dimension: sku       { label: "SKU" type: string sql: ${TABLE}.sku ;; }
  dimension: produit   { label: "Produit" type: string sql: ${TABLE}.product_name ;; }
  dimension: categorie { label: "Catégorie" type: string sql: ${TABLE}.category ;; }
  dimension: prix_catalogue { label: "Prix catalogue" type: number sql: ${TABLE}.price ;; value_format_name: eur }
  dimension: est_actif { label: "Produit actif" type: yesno sql: ${TABLE}.is_active ;; }
}
