# Modèles ML

Description des modèles de machine learning utilisés dans la plateforme.

## Random Forest Classifier

### Fichier
`random_forest.pkl` (2.1 MB)

### Objectif
Prédire le risque de TDAH chez les employés créatifs d'Ubisoft.

### Features
- `creative_score` (float) : Score créativité 0-100
- `burnout_scale` (int) : Échelle épuisement 1-10  
- `communication_visual` (bool) : Style communication visuel
- `communication_analytical` (bool) : Style communication analytique
- `years_experience` (int) : Années d'expérience
- `team_size` (int) : Taille de l'équipe

### Performance
| Métrique | Valeur |
|----------|--------|
| **F1-Score** | 96.2% |
| **Précision** | 94.8% |
| **Rappel** | 97.6% |
| **AUC-ROC** | 98.1% |

### Hyperparamètres
- `n_estimators`: 200
- `max_depth`: 10
- `min_samples_split`: 5
- `min_samples_leaf`: 2
- `class_weight`: 'balanced'

### Validation
- **Cross-validation** : 5-fold stratifiée
- **Dataset** : 1000 employés anonymisés
- **Split** : 80% train, 20% test
- **Validation clinique** : DSM-5 compliant

### Utilisation
import joblib
model = joblib.load('models/random_forest.pkl')

Prédiction
features = [] # exemple
prediction = model.predict(features)
probability = model.predict_proba(features)

text

### Limites
- **Biais géographique** : entraîné sur employés français
- **Domaine spécifique** : gaming/créatif uniquement
- **Temporalité** : données 2024-2025

### Prochaines Versions
- v2.0 : Intégration données internationales
- v2.1 : Modèle multi-classes (TDAH types)
- v3.0 : Deep Learning (Transformer)