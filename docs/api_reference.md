# API Reference

Documentation complète de l'API Ubisoft People Analytics.

## Base URL
http://localhost:8000/api/v1

text

## Authentication
Toutes les requêtes nécessitent un token JWT dans l'header :
Authorization: Bearer <your_token>

text

## Endpoints

### Health Check
**GET** `/health`

Vérifier l'état de l'API.

**Response:**
{
"status": "healthy
, "timestamp": "2025-08-27T12:00:
text

### Prédictions TDAH

**POST** `/predict/adhd`

Prédire le risque TDAH pour un employé.

**Request Body:**
{
"employee_id": "E001
, "creative_score":
85, "burnout_scal
": 3, "communication_style":
text

**Response:**
{
"employee_id": "E001
, "adhd_risk"
0, "probability":
0.23, "confidence":
"high", "recommend
tions": [ "Environnement calm
recommandé", "Pauses fréq
e
text

### Analytics Équipe

**GET** `/analytics/team/{team_id}`

Obtenir les métriques d'une équipe.

**Parameters:**
- `team_id` (string): ID de l'équipe

**Response:**
{
"team_id": "design_team_01
, "total_employees":
25, "neurodivergent_percentage
: 32, "productivity_sco
e": 87, "retention
text

### Recommandations RH

**GET** `/recommendations/{employee_id}`

Obtenir les recommandations RH personnalisées.

**Response:**
{
"employee_id": "E001
, "accommodations
:
[ { "type"
"workspace", "description": "Bureau calme ave
éclairage adapté"


"priority": "high"
], "training_suggestions"
[ "Formation gestion du
t
text

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Données invalides |
| 401 | Unauthorized - Token manquant/invalide |
| 404 | Not Found - Ressource non trouvée |
| 500 | Internal Server Error - Erreur serveur |

## Rate Limiting
- 100 requêtes par minute par IP
- 1000 requêtes par heure par token
