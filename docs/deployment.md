# Guide de Déploiement

Instructions pour déployer Ubisoft People Analytics en production.

## Prérequis

- Docker & Docker Compose
- Kubernetes (optionnel)
- PostgreSQL 14+
- Redis 6+

## Déploiement Local

### 1. Configuration
cp .env.example .env

Modifier les variables dans .env


### 2. Lancement avec Docker Compose
docker-compose up -d --build


### 3. Vérification
- App: http://localhost:8501
- API: http://localhost:8000/docs
- MLflow: http://localhost:5000

## Déploiement Kubernetes

### 1. Créer les secrets
kubectl create secret generic db-credentials
--from-literal=url=postgresql://user:pass@db:5432/ubisoft



### 2. Appliquer les manifests
kubectl apply -f deployment/k8s/


### 3. Vérifier le déploiement
kubectl get pods -l app=ubisoft-analytics
kubect



## Variables d'Environnement

| Variable | Description | Défaut |
|----------|-------------|---------|
| `DATABASE_URL` | URL PostgreSQL | postgresql://localhost/db |
| `REDIS_URL` | URL Redis | redis://localhost:6379 |
| `MLFLOW_TRACKING_URI` | URI MLflow | http://localhost:5000 |
| `SECRET_KEY` | Clé JWT | généré aléatoirement |

## Monitoring

### Healthchecks
- API: `/health`
- Database: connection pooling
- Redis: ping/pong

### Logs
Docker Compose
docker-compose logs -f app

Kubernetes
kubectl logs -f deployment/ubisoft-people-analytics



## Sauvegarde

### Base de données
pg_dump -h localhost -U postgres ubisoft_analytics > backup.sql



### Modèles ML
Les modèles sont versionnés dans MLflow et sauvegardés automatiquement.

## Mise à jour

### Rolling update Kubernetes
kubectl set image deployment/ubisoft-people-analytics
analytics-app=ghcr.io/remichenouri/ubisoft_people_analytics:v2.0.0



### Zero-downtime avec Docker
docker-compose pull
docker-compose
