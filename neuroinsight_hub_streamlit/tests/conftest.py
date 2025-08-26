import pytest
import pandas as pd
from unittest.mock import Mock

@pytest.fixture
def sample_employee_data():
    """Données d'employés fictives pour les tests."""
    return pd.DataFrame({
        'employee_id': ['E001', 'E002', 'E003'],
        'creative_score': [85, 72, 91],
        'burnout_scale': [3, 6, 2],
        'adhd_risk': [0, 1, 0]
    })

@pytest.fixture
def mock_model():
    """Mock d'un modèle ML pour les tests."""
    model = Mock()
    model.predict.return_value = [0, 1, 0]
    model.predict_proba.return_value = [[0.8, 0.2], [0.3, 0.7], [0.9, 0.1]]
    return model
