# KPI de Satisfaction Client

## Description
Le KPI de satisfaction client mesure le degré de satisfaction global des clients basé sur l'analyse de sentiment de leurs feedbacks.

## Calcul
- **Source de données** : Analyse de sentiment des feedbacks clients (table `feedback`)
- **Score de sentiment** : Valeur entre -1 (très négatif) et +1 (très positif)
- **Conversion** : `Score de satisfaction = (sentiment_score + 1) × 50`
- **Résultat** : Pourcentage entre 0% et 100%

## Niveaux de satisfaction
- **Élevé** : ≥ 70% (clients très satisfaits)
- **Moyen** : 50-69% (satisfaction modérée)
- **Faible** : < 50% (clients insatisfaits)

## Affichage
Le KPI est affiché dans le dashboard principal avec :
- Le score en pourcentage
- Le niveau de satisfaction (Élevé/Moyen/Faible)
- Une carte bleue distinctive

## Utilisation
Ce KPI permet de :
- Suivre l'évolution de la satisfaction client dans le temps
- Identifier rapidement les périodes de baisse de satisfaction
- Corréler la satisfaction avec le taux de churn
- Prendre des actions préventives pour améliorer l'expérience client
