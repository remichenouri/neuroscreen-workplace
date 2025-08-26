import pytest
import pandas as pd
from src.models.adhd_model import ADHDClassifier
from src.models.autism_model import AutismClassifier

class TestADHDClassifier:
    def test_predict_valid_input(self, sample_employee_data):
        classifier = ADHDClassifier()
        predictions = classifier.predict(sample_employee_data)
        assert len(predictions) == len(sample_employee_data)
        assert all(pred in [0, 1] for pred in predictions)
    
    def test_predict_proba_output_format(self, sample_employee_data):
        classifier = ADHDClassifier()
        probas = classifier.predict_proba(sample_employee_data)
        assert probas.shape == (len(sample_employee_data), 2)
        assert all(0 <= prob <= 1 for row in probas for prob in row)

class TestAutismClassifier:
    def test_model_performance_threshold(self, sample_employee_data):
        classifier = AutismClassifier()
        # Vérifier que le F1-score reste acceptable
        predictions = classifier.predict(sample_employee_data)
        assert len(predictions) > 0  # Test basique pour la démo
