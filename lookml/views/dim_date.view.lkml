view: dim_date {
  sql_table_name: `portfolio-data-vr.marts.dim_date` ;;
  label: "Calendrier"

  dimension: date_key { primary_key: yes hidden: yes type: number sql: ${TABLE}.date_key ;; }
  dimension: mois_nom { label: "Mois (nom)" type: string sql: ${TABLE}.mois_nom ;; order_by_field: mois_num }
  dimension: mois_num { hidden: yes type: number sql: ${TABLE}.mois_num ;; }
  dimension: jour_semaine {
    label: "Jour de la semaine"
    type: string
    sql: ${TABLE}.jour_semaine_nom ;;
    order_by_field: jour_semaine_num
  }
  dimension: jour_semaine_num { hidden: yes type: number sql: ${TABLE}.jour_semaine_num ;; }
  dimension: est_weekend { label: "Week-end" type: yesno sql: ${TABLE}.est_weekend ;; }
}
