"""
API endpoints pour Ubisoft People Analytics.
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
import json
import logging
from datetime import datetime

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialiser FastAPI
app = FastAPI(
    title="Ubisoft People Analytics API",
    description="API pour la détection de neurodiversité et analytics RH",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chargement du modèle au démarrage
MODEL_DIR = Path("models")
model = None
metadata = None

@app.on_event("startup")
async def load_model():
    """Charger le modèle au démarrage de l'API."""
    global model, metadata
    try:
        model = joblib.load(MODEL_DIR / "random_forest.pkl")
        with open(MODEL_DIR / "model_metadata.json", 'r') as f:
            metadata = json.load(f)
        logger.info("Modèle chargé avec succès")
    except Exception as e:
        logger.error(f"Erreur chargement modèle: {e}")
        raise

# Modèles Pydantic
class EmployeeData(BaseModel):
    """Données d'un employé pour prédiction."""
    employee_id: str = Field(..., description="ID unique de l'employé")
    creative_score: float = Field(..., ge=0, le=100, description="Score créativité 0-100")
    burnout_scale: int = Field(..., ge=1, le=10, description="Échelle burnout 1-10")
    department: Optional[str] = Field(None, description="Département")
    communication_style: Optional[str] = Field(None, description="Style de communication")
    
class PredictionResponse(BaseModel):
    """Réponse de prédiction."""
    employee_id: str
    adhd_risk: int
    probability: float
    confidence: str
    recommendations: List[str]
    timestamp: datetime

class TeamAnalytics(BaseModel):
    """Analytics d'équipe."""
    team_id: str
    total_employees: int
    neurodivergent_percentage: float
    productivity_score: float
    retention_rate: float
    risk_factors: List[str]

class HealthResponse(BaseModel):
    """Réponse health check."""
    status: str
    timestamp: datetime
    model_loaded: bool
    version: str

# Endpoints

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check de l'API."""
    return HealthResponse(
        status="healthy" if model is not None else "unhealthy",
        timestamp=datetime.now(),
        model_loaded=model is not None,
        version="1.0.0"
    )

@app.get("/model/info")
async def get_model_info():
    """Informations sur le modèle chargé."""
    if metadata
