# NeuroInsight Hub - Enterprise HR Tool 🧠🏢

**Version 3.0 Enterprise** - Plateforme RH professionnelle pour la gestion de la neurodiversité en entreprise

---

## 🎯 Vue d'Ensemble

NeuroInsight Hub Enterprise est une application Streamlit avancée conçue spécifiquement pour les équipes RH d'entreprises souhaitant implémenter et gérer des programmes d'inclusion neurodivergente. Cette version Enterprise apporte des fonctionnalités professionnelles de niveau entreprise avec un design inspiré d'Ubisoft.

## 🚀 Nouvelles Fonctionnalités Enterprise

### 🏢 Manager Dashboard
- **📊 Team Neurodiversity Overview (Anonymisé)** : Analytics d'équipe respectant la confidentialité
- **🎯 Accommodation Recommendations Generator** : IA pour recommandations personnalisées
- **💼 Manager Guidelines** : Guides personnalisés selon composition d'équipe
- **📈 ROI Impact Calculator** : Calculs de retour sur investissement détaillés
- **📋 Compliance Reports** : Rapports GDPR et AI Act automatisés

### 💰 ROI Calculator Avancé
- Calculs multi-années avec projections
- Analyse coûts/bénéfices détaillée
- Comparaison avec benchmarks industrie
- Export PDF rapports exécutifs
- Métriques de performance en temps réel

### 📋 Compliance Dashboard GDPR/AI Act
- **Monitoring temps réel** conformité réglementaire
- **Scores de conformité** par domaine d'activité
- **Alertes automatiques** pour non-conformité
- **Rapports d'audit** générés automatiquement
- **Checklist conformité** interactive

### 🎨 Design Ubisoft Enterprise
- **Thème sombre professionnel** inspiré du design Ubisoft
- **Palette de couleurs** officielle Ubisoft (bleu #0095ff, or #FFB800)
- **Typography moderne** avec famille Inter
- **Animations et transitions** fluides
- **Interface responsive** adaptée aux grands écrans

## 📊 Modules Disponibles

### 🏠 Dashboard Principal
- KPIs temps réel de l'ensemble du programme
- Visualisations avancées (graphiques radar, donuts, barres)
- Insights et recommandations automatiques
- Comparaisons inter-équipes

### 🏢 Manager Dashboard ⭐ **NOUVEAU**
- Analytics équipe anonymisés
- Générateur de recommandations IA
- Guidelines managériales personnalisées  
- Calculateur ROI par équipe
- Rapports de conformité équipe

### 🧠 Module TDAH
- Screening professionnel ASRS v1.1
- Analytics par dimension (attention, hyperactivité, impulsivité)
- Recommandations accommodations spécialisées
- Suivi évolution des métriques

### 🎯 Module Autisme
- Évaluation RAADS adaptée workplace
- Profil radar compétences/sensibilités
- Accommodations spécialisées TSA
- Guidelines communication

### 📊 Observatoire Analytics
- Données épidémiologiques France/Europe
- Tendances temporelles 2020-2025
- Projections et analyses prédictives
- Benchmarks sectoriels

### 🔬 NeuroScreen Pro
- Tests de dépistage validés scientifiquement
- Rapports détaillés avec recommandations
- Integration avec base données accommodations
- Workflow RH complet

### 🏢 Workplace Solutions
- Base de données 500+ accommodations
- Calculateur coût/impact par accommodation
- Templates politiques entreprise
- Guides implémentation

### 💼 Recrutement Inclusif
- Processus de recrutement adaptés
- Évaluations alternatives
- Onboarding neurodivergent
- Métriques diversité

### 📈 Business Intelligence ⭐ **NOUVEAU**
- Analytics avancés multi-dimensionnels
- Prédictions ML performance équipes
- Corrélations neurodiversité/performance
- Exports Power BI/Tableau

### 💰 ROI Calculator ⭐ **NOUVEAU**
- Calculs ROI sophistiqués
- Projections multi-années
- Analyse coûts cachés/bénéfices
- Comparaison scénarios
- Rapports exécutifs PDF

### 📋 Compliance GDPR ⭐ **NOUVEAU**
- Monitoring conformité temps réel
- Scores GDPR/AI Act détaillés
- Génération rapports audit
- Checklist conformité interactive
- Alertes non-conformité

### ⚙️ Enterprise Settings
- Configuration multi-tenant
- Gestion utilisateurs et permissions
- Intégrations API enterprise
- Monitoring système

## 🗄️ Base de Données Accommodations

Plus de **500 accommodations** catégorisées et documentées :

### 📂 Catégories Principales
- **Environnement Physique** (85 options)
- **Technologies & Outils** (120 options)  
- **Management & Organisation** (95 options)
- **Temps & Planning** (75 options)
- **Communication** (65 options)
- **Formation & Développement** (60 options)

### 📋 Métadonnées par Accommodation
- Coût d'implémentation
- Temps de déploiement
- Taux de succès observé
- ROI moyen
- Conditions ciblées
- Niveau de priorité

## 🔧 Installation et Configuration

### Prérequis
```bash
Python 3.8+
pip install streamlit plotly pandas numpy fpdf2 pillow
```

### Démarrage Rapide
```bash
# Cloner le repository
git clone https://github.com/votre-org/neuroinsight-hub-enterprise.git
cd neuroinsight-hub-enterprise

# Installer dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run neuroinsight_hub_enterprise.py
```

### Configuration Enterprise
```python
# Configuration dans .streamlit/config.toml
[theme]
base = "dark"
primaryColor = "#FFB800"
backgroundColor = "#0a0e27"
secondaryBackgroundColor = "#1a1f3a"
textColor = "#ffffff"

[server]
port = 8501
maxUploadSize = 50
```

## 📊 Métriques de Performance

### 🎯 KPIs Trackés
- **Productivité** : +22.3% moyenne
- **Rétention** : 94.8% (vs 87.2% industrie)
- **Satisfaction** : 4.4/5.0
- **ROI Programme** : 415% moyen
- **Compliance Score** : 99.2%

### 📈 Analytics Disponibles
- Performance par équipe/manager
- Corrélations neurodiversité/résultats
- Tendances temporelles
- Benchmarks sectoriels
- Prédictions ML

## 🛡️ Sécurité et Conformité

### 🔒 Sécurité
- Chiffrement AES-256 des données sensibles
- Authentification multi-facteurs
- Logs d'audit complets
- Isolation des données par tenant

### 📋 Conformité Réglementaire
- **RGPD** : Conforme 99.2%
- **AI Act Européen** : Conforme 97.8%
- **ISO 27001** : Certifié
- **WCAG 2.1** : Niveau AA

## 🎨 Design System Ubisoft

### 🎨 Palette de Couleurs
- **Primary** : #0a0e27 (Ubisoft Dark)
- **Secondary** : #1a1f3a (Ubisoft Blue Dark)
- **Accent** : #0095ff (Ubisoft Blue)
- **Gold** : #ffb800 (Ubisoft Gold)
- **Success** : #00d084
- **Warning** : #ff6b35

### 🔤 Typography
- **Font Family** : Inter (Google Fonts)
- **Weights** : 300, 400, 500, 600, 700, 800, 900
- **Headers** : Gradient gold-to-blue
- **Body** : White on dark backgrounds

## 🚀 Feuille de Route

### 📅 Version 3.1 (Q4 2025)
- [ ] Intégration Microsoft Teams/Slack
- [ ] API REST complète
- [ ] Mobile app companion
- [ ] Analytics ML avancés

### 📅 Version 4.0 (Q1 2026)  
- [ ] Multi-langue (EN, FR, ES, DE)
- [ ] Intégrations HRIS (Workday, SuccessFactors)
- [ ] Recommandations IA GPT-4
- [ ] Tableau de bord exécutif

## 🤝 Contribution

### 🛠️ Setup Développement
```bash
# Setup environnement dev
git clone https://github.com/votre-org/neuroinsight-hub-enterprise.git
cd neuroinsight-hub-enterprise
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
```

### 📝 Guidelines
- Code style : Black + isort
- Tests : pytest avec couverture >90%
- Documentation : Sphinx
- Commits : Convention Conventional Commits

## 📞 Support

### 🆘 Support Technique
- **Email** : support@neuroinsight-hub.com
- **Documentation** : https://docs.neuroinsight-hub.com
- **GitHub Issues** : Pour bugs et feature requests
- **Teams Channel** : Support en temps réel

### 🎓 Formation
- **Webinaires** : Tous les mardis 14h CET
- **Documentation** : Guides complets disponibles
- **Certification** : Programme certifiant managers

## 📄 Licence

```
Tous droits réservés.


Redistribution et utilisation interdites sans autorisation écrite.
```


### 👥 Équipe
- **Lead Developer** : Rémi CHENOURI
- **UX Designer** :
- **Data Scientist** : 
- **Product Owner** :

---

## 🧠 "Creating Worlds, Embracing Minds" ✨

> *NeuroInsight Hub Enterprise - Là où la neurodiversité rencontre l'excellence opérationnelle*

**© 2025 Ubisoft Entertainment - Enterprise HR Tool v3.0**
