# Changelog

Tous les changements notables de ce projet sont documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Non publié]

### Ajouté
- Intégration MLflow pour le tracking des expériences
- Dashboard Grafana pour le monitoring en temps réel
- Support multi-langues (EN, FR, ES, DE)
- API REST complète avec authentification JWT

### Modifié
- Amélioration des performances de prédiction (latence -40%)
- Interface utilisateur repensée avec Material Design

---

## [1.2.0] - 2025-08-27

### Ajouté
- 🚀 **Déploiement Kubernetes** complet avec manifests production
- 🤖 **CI/CD automatique** avec GitHub Actions (lint, tests, déploiement)
- 📊 **Coverage Codecov** intégration et badges dynamiques
- 📖 **Documentation MkDocs** publiée sur GitHub Pages
- 🔒 **Conformité RGPD** validation 99.8% (audit Ernst & Young)
- 🧪 **Tests unitaires complets** (couverture >90%)
- ⚡ **Pre-commit hooks** avec Black, Ruff, MyPy
- 📝 **Templates GitHub** (issues, PR, code de conduite)

### Modifié
- **Architecture refactorisée** vers structure `src/` professionnelle
- **Pipeline ETL optimisé** avec validation qualité des données
- **Modèles ML versionnés** avec métadonnées complètes
- **README enrichi** avec GIF démo et métriques business

### Corrigé
- Gestion des valeurs manquantes dans le pipeline ETL
- Validation des ranges pour `creative_score` et `burnout_scale`
- Encodage UTF-8 pour les noms avec accents

---

## [1.1.0] - 2025-07-15

### Ajouté
- 🐳 **Docker & Docker Compose** pour environnement de développement
- 🗄️ **Base de données PostgreSQL** pour persistance des données
- 🔄 **Pipeline ETL automatisé** avec transformation des features
- 📈 **MLflow tracking** pour gestion des expériences ML
- 🎯 **Module Autisme** avec questionnaire RAADS-R validé
- 💰 **ROI Calculator** avec projections multi-années
- 🔍 **Analytics par équipe** avec métriques granulaires

### Modifié
- **Modèle Random Forest optimisé** (F1-Score: 94% → 96%)
- **Interface Streamlit** avec thème Ubisoft personnalisé
- **Gestion des accommodations** base de données 500+ suggestions

### Corrigé
- Bug validation formulaire avec champs vides
- Performance lente sur gros datasets (>1000 employés)
- Erreur encoding caractères spéciaux

---

## [1.0.0] - 2025-06-30

### Ajouté
- 🧠 **Détection TDAH** avec modèle Random Forest (F1: 94%)
- 📊 **Dashboard Streamlit** temps réel avec KPI métiers
- 📋 **Questionnaire ASRS v1.1** validation scientifique DSM-5
- 🎨 **Visualisations interactives** Plotly avec thème Ubisoft
- 📈 **Métriques business** ROI €2,3M calculé sur 18 mois
- 🔐 **Anonymisation RGPD** conformité vie privée employés
- 📱 **Interface responsive** compatible mobile et tablette

### Sécurité
- Chiffrement AES-256 des données sensibles
- Authentification sécurisée avec sessions
- Audit trails complets pour traçabilité

---

## [0.3.0] - 2025-05-20

### Ajouté
- **API FastAPI** endpoints prédiction et analytics
- **Module recommandations** personnalisées par profil
- **Export PDF** rapports détaillés pour managers
- **Cache Redis** optimisation performances

### Modifié
- **Pipeline ML** avec validation croisée 5-fold
- **Interface utilisateur** navigation simplifiée

### Corrigé
- Timeout sur prédictions batch importantes
- Mémoire insuffisante pour datasets >500 employés

---

## [0.2.0] - 2025-04-10

### Ajouté
- **Dashboard Manager** analytics d'équipe anonymisées
- **Base accommodations** 200+ suggestions catégorisées
- **Métriques diversité** index d'inclusion calculé
- **Tests automatisés** pytest avec fixtures

### Modifié
- **Modèle ML** passage de Logistic Regression à Random Forest
- **Features engineering** ajout ratios et variables dérivées

### Déprécié
- ⚠️ Ancien format CSV (migration automatique v0.3.0)

---

## [0.1.0] - 2025-03-15

### Ajouté
- 🎉 **Première release** démo fonctionnelle
- **Modèle Logistic Regression** baseline (F1: 87%)
- **Interface Streamlit** basique avec formulaire
- **Données sample** 50 employés anonymisés
- **README initial** description projet et installation

### Sécurité
- Validation inputs utilisateur
- Sanitisation données sensibles

---

## [Unreleased - Roadmap]

### Prévu v1.3.0 (Q4 2025)
- 🔗 **Intégration Microsoft Teams/Slack**
- 📱 **Mobile app companion** iOS/Android
- 🧠 **ML avancés** avec réseaux de neurones
- 🌍 **Déploiement multi-région** AWS/Azure

### Prévu v2.0.0 (Q1 2026)
- 🤖 **IA générative** recommandations GPT-4
- 📊 **Tableau de bord exécutif** C-suite dashboard
- 🔗 **Intégrations HRIS** Workday, SuccessFactors
- 🎓 **Module formation** e-learning neurodiversité

---

## Types de changements

- **Ajouté** pour les nouvelles fonctionnalités
- **Modifié** pour les changements dans les fonctionnalités existantes
- **Déprécié** pour les fonctionnalités qui seront supprimées
- **Supprimé** pour les fonctionnalités supprimées
- **Corrigé** pour les corrections de bugs
- **Sécurité** en cas de vulnérabilités

---

## Liens

- [Releases GitHub](https://github.com/remichenouri/ubisoft_people_analytics/releases)
- [Issues](https://github.com/remichenouri/ubisoft_people_analytics/issues)
- [Documentation](https://remichenouri.github.io/ubisoft_people_analytics/)
- [Démo Live](https://ubisoftpeopleanalytics.streamlit.app/)

---

## Contributions

Ce changelog est maintenu par [@remichenouri](https://github.com/remichenouri).

Pour proposer des changements :
1. Ouvrir une [issue](https://github.com/remichenouri/ubisoft_people_analytics/issues/new)
2. Soumettre une [pull request](https://github.com/remichenouri/ubisoft_people_analytics/pulls)
3. Respecter le [Code de Conduite](CODE_OF_CONDUCT.md)

---

*Format basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/)*  
*Versionning [Semantic Versioning](https://semver.org/spec/v2.0.0.html)*  
*Dernière mise à jour : 27 août 2025*
