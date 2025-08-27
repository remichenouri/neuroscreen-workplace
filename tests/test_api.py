"""
Tests pour l'API FastAPI.
"""

import pytest
import pandas as pd
import numpy as np
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import json

from src.api.endpoints import app

client = TestClient(app)

class TestHealthEndpoint:
    """Tests pour l'endpoint health."""
    
    def test_health_check_with_model_loaded(self):
        """Test health check avec modèle chargé."""
        with patch('src.api.endpoints.model', MagicMock()):
            response = client.get("/health")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["model_loaded"] is True
            assert "timestamp" in data
    
    def test_health_check_without_model(self):
        """Test health check sans modèle."""
        with patch('src.api.endpoints.model', None):
            response = client.get("/health")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "unhealthy"
            assert data["model_loaded"] is False

class TestPredictionEndpoint:
    """Tests pour l'endpoint de prédiction."""
    
    @pytest.fixture
    def mock_model(self):
        """Mock du modèle ML."""
        model = MagicMock()
        model.predict.return_value = np.array([1])
        model.predict_proba.return_value = np.array([[0.2, 0.8]])
        return model
    
    @pytest.fixture
    def valid_employee_data(self):
        """Données d'employé valides."""
        return {
            "employee_id": "E001",
            "creative_score": 85.5,
            "burnout_scale": 7,
            "department": "design",
            "communication_style": "visual"
        }
    
    def test_predict_adhd_success(self, mock_model, valid_employee_data):
        """Test prédiction TDAH réussie."""
        with patch('src.api.endpoints.model', mock_model):
            response = client.post("/api/v1/predict/adhd", 
                                 json=valid_employee_data)
            
            assert response.status_code == 200
            data = response.json()
            
            assert data["employee_id"] == "E001"
            assert data["adhd_risk"] == 1
            assert 0 <= data["probability"] <= 1
            assert data["confidence"] in ["faible", "modérée", "élevée", "très_élevée"]
            assert isinstance(data["recommendations"], list)
            assert "timestamp" in data
    
    def test_predict_adhd_invalid_data(self):
        """Test prédiction avec données invalides."""
        invalid_data = {
            "employee_id": "E001",
            "creative_score": 150,  # Hors range
            "burnout_scale": 15     # Hors range
        }
        
        response = client.post("/api/v1/predict/adhd", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_predict_adhd_missing_fields(self):
        """Test prédiction avec champs manquants."""
        incomplete_data = {
            "employee_id": "E001"
            # Champs requis manquants
        }
        
        response = client.post("/api/v1/predict/adhd", json=incomplete_data)
        assert response.status_code == 422
    
    def test_predict_adhd_model_error(self, valid_employee_data):
        """Test erreur du modèle."""
        mock_model = MagicMock()
        mock_model.predict.side_effect = Exception("Erreur modèle")
        
        with patch('src.api.endpoints.model', mock_model):
            response = client.post("/api/v1/predict/adhd", 
                                 json=valid_employee_data)
            
            assert response.status_code == 500

class TestTeamAnalyticsEndpoint:
    """Tests pour l'endpoint d'analytics d'équipe."""
    
    @pytest.fixture
    def mock_team_data(self):
        """Données d'équipe simulées."""
        return pd.DataFrame({
            'employee_id': ['E001', 'E002', 'E003'],
            'creative_score': [85, 72, 91],
            'burnout_scale': [3, 6, 2],
            'adhd_risk': [0, 1, 0],
            'department': ['design', 'design', 'design']
        })
    
    def test_get_team_analytics_success(self, mock_team_data):
        """Test analytics d'équipe réussie."""
        with patch('src.api.endpoints.get_team_data') as mock_get_team:
            mock_get_team.return_value = mock_team_data
            
            response = client.get("/api/v1/analytics/team/design_team_01")
            
            assert response.status_code == 200
            data = response.json()
            
            assert data["team_id"] == "design_team_01"
            assert data["total_employees"] == 3
            assert "neurodivergent_percentage" in data
            assert "productivity_score" in data
    
    def test_get_team_analytics_not_found(self):
        """Test équipe non trouvée."""
        with patch('src.api.endpoints.get_team_data') as mock_get_team:
            mock_get_team.return_value = pd.DataFrame()  # Équipe vide
            
            response = client.get("/api/v1/analytics/team/nonexistent_team")
            
            assert response.status_code == 404

class TestRecommendationsEndpoint:
    """Tests pour l'endpoint de recommandations."""
    
    def test_get_recommendations_success(self):
        """Test récupération de recommandations réussie."""
        mock_recommendations = {
            "employee_id": "E001",
            "accommodations": [
                {
                    "type": "workspace",
                    "description": "Bureau calme avec éclairage adapté",
                    "priority": "high"
                }
            ],
            "training_suggestions": [
                "Formation gestion du stress",
                "Techniques de concentration"
            ]
        }
        
        with patch('src.api.endpoints.generate_recommendations') as mock_gen:
            mock_gen.return_value = mock_recommendations
            
            response = client.get("/api/v1/recommendations/E001")
            
            assert response.status_code == 200
            data = response.json()
            
            assert data["employee_id"] == "E001"
            assert "accommodations" in data
            assert "training_suggestions" in data

class TestModelInfoEndpoint:
    """Tests pour l'endpoint d'informations du modèle."""
    
    def test_get_model_info_success(self):
        """Test récupération des infos du modèle."""
        mock_metadata = {
            "model_name": "RandomForest",
            "training_date": "2025-08-27T10:00:00",
            "metrics": {
                "f1_score": 0.96,
                "accuracy": 0.94
            }
        }
        
        with patch('src.api.endpoints.metadata', mock_metadata):
            response = client.get("/api/v1/model/info")
            
            assert response.status_code == 200
            data = response.json()
            
            assert data["model_name"] == "RandomForest"
            assert "training_date" in data
            assert "metrics" in data

class TestErrorHandling:
    """Tests de gestion d'erreurs."""
    
    def test_internal_server_error(self):
        """Test erreur serveur interne."""
        with patch('src.api.endpoints.model') as mock_model:
            mock_model.predict.side_effect = Exception("Erreur critique")
            
            valid_data = {
                "employee_id": "E001",
                "creative_score": 85.0,
                "burnout_scale": 5
            }
            
            response = client.post("/api/v1/predict/adhd", json=valid_data)
            
            assert response.status_code == 500
            assert "error" in response.json()
    
    def test_invalid_json(self):
        """Test JSON invalide."""
        response = client.post("/api/v1/predict/adhd", 
                             data="invalid json")
        
        assert response.status_code == 422

class TestAuthentication:
    """Tests d'authentification (si implémentée)."""
    
    @pytest.mark.skip("Authentification non encore implémentée")
    def test_protected_endpoint_without_token(self):
        """Test endpoint protégé sans token."""
        response = client.get("/api/v1/admin/users")
        assert response.status_code == 401
    
    @pytest.mark.skip("Authentification non encore implémentée")
    def test_protected_endpoint_with_invalid_token(self):
        """Test endpoint protégé avec token invalide."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/v1/admin/users", headers=headers)
        assert response.status_code == 401

@pytest.fixture
def sample_employee_data():
    """Données d'employé pour les tests."""
    return pd.DataFrame({
        'employee_id': ['E001', 'E002', 'E003'],
        'creative_score': [85, 72, 91],
        'burnout_scale': [3, 6, 2],
        'adhd_risk': [0, 1, 0]
    })

def test_api_integration_flow(sample_employee_data):
    """Test d'intégration complet de l'API."""
    
    # Test 1: Health check
    response = client.get("/health")
    assert response.status_code == 200
    
    # Test 2: Model info (si modèle chargé)
    with patch('src.api.endpoints.metadata', {"model_name": "test"}):
        response = client.get("/api/v1/model/info")
        assert response.status_code == 200
    
    # Test 3: Prédiction
    employee_data = {
        "employee_id": "E001",
        "creative_score": 85.0,
        "burnout_scale": 5
    }
    
    with patch('src.api.endpoints.model') as mock_model:
        mock_model.predict.return_value = np.array([0])
        mock_model.predict_proba.return_value = np.array([[0.8, 0.2]])
        
        response = client.post("/api/v1/predict/adhd", json=employee_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "prediction" in data or "adhd_risk" in data
        assert "probability" in data

if __name__ == "__main__":
    pytest.main([__file__])
