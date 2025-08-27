"""Configuration pytest et fixtures communes."""

import pytest
import pandas as pd
from pathlib import Path

@pytest.fixture
def sample_data():
    """Données d'exemple pour les tests."""
    return pd.DataFrame({
        'employee_id': ['E001', 'E002', 'E003'],
        'creative_score': [85, 72, 91],
        'burnout_scale': [3, 6, 2],
        'adhd_risk': [0, 1, 0]
    })

@pytest.fixture
def test_data_dir(tmp_path):
    """Répertoire temporaire pour les tests."""
    data_dir = tmp_path / "test_data"
    data_dir.mkdir()
    return data_dir
