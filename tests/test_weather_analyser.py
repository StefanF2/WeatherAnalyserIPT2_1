import os
import sys
import pytest
 
# Sicherstellen, dass src/ im Pfad ist
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from weather_analyser import csv_einlesen, merge, merge_sort, calculate_stats, header, main



# T01
def test_csv_einlesen():
    data = csv_einlesen("test_wetterdaten.csv")
    assert isinstance(data, list) 
# T02
def test_csv_einlesen_länge():
    data = csv_einlesen("test_wetterdaten.csv")
    assert len(data) == 7
# T03
def test_csv_einlesen_kopfzeile():
    data = csv_einlesen("test_wetterdaten_kopfzeilefehlt.csv")
    assert data == []

# T04
def test_merge_sort_normal():

    daten = [
        {"wert": 3},
        {"wert": 1},
        {"wert": 4},
        {"wert": 1},
        {"wert": 5}
    ]

    result = merge_sort(daten, "wert")

    werte = [x["wert"] for x in result]

    assert werte == [1, 1, 3, 4, 5]

# T05
def test_merge_sort_sortiert():

    daten = [
        {"wert": 1},
        {"wert": 2},
        {"wert": 3}
    ]

    result = merge_sort(daten, "wert")

    werte = [x["wert"] for x in result]

    assert werte == [1, 2, 3]

# T06
def test_merge_sort_umgekehrt():

    daten = [
        {"wert": 5},
        {"wert": 4},
        {"wert": 3},
        {"wert": 2},
        {"wert": 1}
    ]

    result = merge_sort(daten, "wert")

    werte = [x["wert"] for x in result]

    assert werte == [1, 2, 3, 4, 5]
# T07
def test_merge_sort_ein_element():

    daten = [
        {"wert": 42}
    ]

    result = merge_sort(daten, "wert")

    werte = [x["wert"] for x in result]

    assert werte == [42]
# T08
def test_merge_sort_leer():

    result = merge_sort([], "wert")

    assert result == []
# T09
def test_merge_sort_dict_nach_temp():

    daten = [
        {"temp": 15},
        {"temp": 8},
        {"temp": 22},
        {"temp": 10}
    ]

    result = merge_sort(daten, "temp")

    temps = [d["temp"] for d in result]

    assert temps == [8, 10, 15, 22]
# T10
def test_minimum_normal():

    daten = [
        {"temp": 15},
        {"temp": 8},
        {"temp": 22}
    ]

    minimum_item, _, _ = calculate_stats(daten, "temp")

    assert minimum_item == {"temp": 8}
# T11
def test_minimum_ein_element():

    daten = [{"temp": 42}]

    minimum_item, _, _ = calculate_stats(daten, "temp")

    assert minimum_item == {"temp": 42}
# T12
def test_maximum_normal():

    daten = [
        {"temp": 15},
        {"temp": 8},
        {"temp": 22}
    ]

    _, maximum_item, _ = calculate_stats(daten, "temp")

    assert maximum_item == {"temp": 22}
# T13
def test_maximum_gleiche_werte():

    daten = [
        {"temp": 10},
        {"temp": 10},
        {"temp": 10}
    ]

    _, maximum_item, _ = calculate_stats(daten, "temp")

    assert maximum_item == {"temp": 10}
# T14
def test_durchschnitt_normal():

    daten = [
        {"temp": 10},
        {"temp": 20},
        {"temp": 30}
    ]

    _, _, average = calculate_stats(daten, "temp")

    assert average == 20.0
# T15
def test_durchschnitt_leer():

    daten = []

    result = calculate_stats(daten, "temp")

    assert result == (None, None, None)
# T16

def test_durchschnitt_gerundet():

    daten = [
        {"temp": 3.333},
        {"temp": 6.667}
    ]

    _, _, average = calculate_stats(daten, "temp")

    assert round(average, 2) == 5.00