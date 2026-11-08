view: fct_sales {
  sql_table_name: `portfolio-data-vr.marts.fct_sales` ;;
  label: "Ventes"

  # --- Clés (cachées : on navigue par les dimensions jointes) ---
  dimension: ligne_id {
    primary_key: yes
    hidden: yes
    sql: CONCAT(CAST(${TABLE}.order_id AS STRING), '-', CAST(${TABLE}.product_key AS STRING)) ;;
  }
  dimension: customer_key { hidden: yes type: number sql: ${TABLE}.customer_key ;; }
  dimension: product_key  { hidden: yes type: number sql: ${TABLE}.product_key ;; }
  dimension: date_key     { hidden: yes type: number sql: ${TABLE}.date_key ;; }

  # --- Dimensions ---
  dimension: order_id {
    label: "N° de commande"
    type: number
    value_format_name: id
    sql: ${TABLE}.order_id ;;
  }
  dimension_group: commande {
    label: "Commande"
    type: time
    timeframes: [date, week, month, quarter, year]
    datatype: date
    convert_tz: no
    sql: ${TABLE}.order_day ;;
  }
  dimension: statut {
    label: "Statut"
    type: string
    sql: ${TABLE}.status ;;
  }
  dimension: est_annulee {
    label: "Commande annulée"
    type: yesno
    sql: ${TABLE}.status = 'cancelled' ;;
  }
  dimension: quantite { hidden: yes type: number sql: ${TABLE}.quantity ;; }
  dimension: montant_ligne { hidden: yes type: number sql: ${TABLE}.line_amount ;; }

  # --- Mesures ---
  # La règle « hors annulées » est écrite une seule fois, ici, et seulement sur les mesures où elle vaut.
  # C'est la leçon de la Q3 de l'évaluation : une règle métier doit dire à quoi elle s'applique.

  measure: chiffre_affaires {
    label: "Chiffre d'affaires"
    description: "Somme des montants de ligne, hors commandes annulées."
    type: sum
    sql: ${montant_ligne} ;;
    filters: [est_annulee: "no"]
    value_format_name: eur
  }
  measure: quantite_vendue {
    label: "Quantité vendue"
    description: "Articles vendus, hors commandes annulées."
    type: sum
    sql: ${quantite} ;;
    filters: [est_annulee: "no"]
  }
  measure: nb_commandes {
    label: "Commandes (tous statuts)"
    description: "Commandes passées, annulées comprises : une commande annulée a bien été passée."
    type: count_distinct
    sql: ${order_id} ;;
  }
  measure: nb_commandes_valides {
    label: "Commandes hors annulées"
    type: count_distinct
    sql: ${order_id} ;;
    filters: [est_annulee: "no"]
  }
  measure: nb_commandes_annulees {
    hidden: yes
    type: count_distinct
    sql: ${order_id} ;;
    filters: [est_annulee: "yes"]
  }
  measure: nb_clients {
    label: "Clients ayant commandé"
    description: "Clients distincts, tous statuts : un client qui n'a que des commandes annulées compte."
    type: count_distinct
    sql: ${customer_key} ;;
  }
  measure: panier_moyen {
    label: "Panier moyen"
    description: "Chiffre d'affaires / commandes hors annulées."
    type: number
    sql: ${chiffre_affaires} / NULLIF(${nb_commandes_valides}, 0) ;;
    value_format_name: eur
  }
  measure: taux_annulation {
    label: "Taux d'annulation"
    description: "Commandes annulées / commandes tous statuts."
    type: number
    sql: ${nb_commandes_annulees} / NULLIF(${nb_commandes}, 0) ;;
    value_format_name: percent_2
  }
}
