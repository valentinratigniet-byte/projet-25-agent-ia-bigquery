view: dim_customer {
  sql_table_name: `portfolio-data-vr.marts.dim_customer` ;;
  label: "Client"

  dimension: customer_key { primary_key: yes hidden: yes type: number sql: ${TABLE}.customer_key ;; }
  dimension: pays {
    label: "Pays"
    type: string
    map_layer_name: countries
    sql: ${TABLE}.country_name ;;
  }
  dimension: code_pays { label: "Code pays" type: string sql: ${TABLE}.country ;; }
  # Données personnelles (fictives ici, mais on les traite comme réelles) : non exposées à l'exploration
  dimension: nom   { hidden: yes type: string sql: ${TABLE}.full_name ;; }
  dimension: email { hidden: yes type: string sql: ${TABLE}.email ;; }
}
