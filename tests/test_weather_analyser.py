import os
import sys
import pytest
 
# Sicherstellen, dass src/ im Pfad ist
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from weather_analyser import csv_einlesen

def test_csv_einlesen():
    data = csv_einlesen("test_wetterdaten.csv")
    assert isinstance(data, list) 
    assert len(data) == 7