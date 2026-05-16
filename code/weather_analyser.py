import csv # Damit man csv Dateien einlesen kann
import os # Damit man Dateipfade finden kann egal wo es liegt

# Hier wird die CSV Datei eingelesen und in einer "Python Liste" gespeichert
def csv_einlesen(file_name):
Liest eine CSV-Datei mit Wetterdaten ein.
"""
    Args:
        file_name: Name der Datei

    Returns:
        list: Liste mit Wetterdaten als Dictionaries

    Raises:
        FileNotFoundError: Wenn die Datei nicht gefunden wird
"""
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Hier wird der Ordner genommen wo innen das Python Skript ist
    root_dir = os.path.dirname(script_dir) # Hier wird der Ordner vorherig genommen von script_dir also der root folder
    file_path = None

    for root, dirs, files in os.walk(root_dir): # Hier werden alle Ordner rekursiv ab root_dir durchsucht 

        if file_name in files: # Falls die CSV Datei gefunden wurde dann wird die in file_path gespeichert
            file_path = os.path.join(root, file_name)
            break

    if file_path is None: # Falls die CSV Datei nicht gefunden wurde kommt eine Fehlermeldung zurück
        raise FileNotFoundError(f"Datei '{file_name}' nicht gefunden")

    data = [] # Diese Liste wird erstellt wo alle Zeilen von der CSV Datei gespeichert werden. 

    with open(file_path, newline="", encoding="utf-8") as file: # Hier wird die CSV Datei geöffnet
        reader = csv.DictReader(file, delimiter=";")            # Hier wird die CSV Datei Zeile für Zeile eingelesen und in einem Dictionary gespeichert
        
        expected_fields = [ #Hier ist die Liste der erwateten Werte in der CSV Datei
            "datum",
            "temperatur",
            "windgeschwindigkeit",
            "schneehoehe"
        ]

        # Prüfen ob Kopfzeile korrekt ist
        if reader.fieldnames is None:
            return []

        if not all(field in reader.fieldnames for field in expected_fields): # Hier wird geprüft ob alle "expected_fields" in der Datei sind
            return []

        for row in reader:  # Hier wird jede Zeile ausgeführt
            data.append({   # Hier werden die Werte von der CSV Datei in die Liste gespeichert. Es wird auch gleich in die richtige Datentypen umgewandelt
                "Datum": row["datum"],
                "Temperatur": float(row["temperatur"]),
                "Windgeschwindigkeit": float(row["windgeschwindigkeit"]),
                "Schneehoehe": float(row["schneehoehe"])
            })

    return data # Hier wird die Liste mit den Werte zurückgegeben


# Hier wird die Merge Funktion definiert welche zwei sotierte listen bekommt und kombiniert. Es wird key gegeben damit die Funktion weiss welche Dateien benutzt werden sollen
def merge(left, right, key):
    """
    Führt zwei sortierte Listen zu einer sortierten Liste zusammen

    Args:
        left (list): Linke sortierte Liste
        right (list): Rechte sortierte Liste
        key (str): Schlüssel für den Vergleich

    Returns:
        list: Zusammengeführte sortierte Liste
    """
    result = [] #Eine neue Liste wird erstellt
    i = j = 0 # i zeigt auf links und j auf rechts

    while i < len(left) and j < len(right): # Diese Schleife läuft solange es noch elemente in left und right gibt
        if left[i][key] < right[j][key]: # Hier wird der Wert der beiden Listen mit dem key (z.B Temperatur) verglichen
            result.append(left[i]) # Das linke Element wird zur result Liste hinzugefügt
            i += 1
        else:
            result.append(right[j]) # Das rechte Element wird zur result Liste hinzugefügt
            j += 1

    result.extend(left[i:]) # Hier werden alle restlichen left Element hinzugefügt
    result.extend(right[j:]) # Hier werden alle restlichen right Elemente hinzugefügt
    return result # Die sortierte Liste wird zurückgegeben


def merge_sort(data, key):
    """
    Sortiert eine Liste mit dem Merge-Sort-Algorithmus

    Args:
        data (list): Unsortierende Liste
        key (str): Schlüssel nach dem sortiert wird

    Returns:
        list: Sortierte Liste
    """
    if len(data) <= 1: # Basisfall, hier wird geprüft ob die Liste schon sotiert ist
        return data

    mid = len(data) // 2 # Mitte der Liste wird berechnet
    left = merge_sort(data[:mid], key) # Linke Hälfte wird sotiert
    right = merge_sort(data[mid:], key) # Rechte Hälfte wird sotiert

    return merge(left, right, key) # Beide sortierten Listen werden kombiniert

# Hier wird Minimum, Maximum und Durchschnitt berechnet.
def calculate_stats(data, key):
    """
    Berechnet Minimum, Maximum und Durchschnitt einer Liste

    Args:
        data (list): Liste mit Wetterdaten
        key (str): Schlüssel für die Berechnung

    Returns:
         Minimum, Maximum und Durchschnitt
    """   
    if not data: # Prüft ob die Datei vorhanden ist
        return None, None, None
    
    values = [item[key] for item in data] # Hier werden alle Werte von dem key in einer Liste gespeichert damit man den Durchschnitt berechnen kann
    

    minimum_item = min(data, key=lambda x: x[key]) # Der kleinste Wert wird gefunden
    maximum_item = max(data, key=lambda x: x[key]) # Der grösste Wert wird gefunden
    average = sum(values) / len(values) # Durchschnitt berechnen

    return minimum_item, maximum_item, average # Ergebnisse werden zurückgegeben

def header(): # Gibt den Header aus
    headerline = "=" * 80 # 80 mal "=" wird in headerline gespeichert
    file_path = os.path.abspath(__file__) # Der genauer File path wird in file_path gespeichert
    print(headerline) 
    print(" Programmname: WeatherAnalyser – Wetterdaten-Auswertung - Bergbahnen Flumserberg AG, Flums")
    print(" Datei Pfad: " + file_path)
    print(headerline)

def main():  #Führt das Hauptprogramm aus und gibt die Daten an
    header()
    data = csv_einlesen("wetterdaten.csv")  # Datei wird geladen
    if not data:
        print("Fehler: Keine Daten vorhanden!") # Falls die datei leer ist oder nicht gefunden wird, wird eine Fehlermeldung ausgegeben

    einheiten = {
    "Temperatur": "°C",
    "Windgeschwindigkeit": "km/h",
    "Schneehoehe": "cm"
}

    keys = ["Temperatur", "Windgeschwindigkeit", "Schneehoehe"] # Die Messwerte werden duchgegangen und die Statistiken werden berechnet und ausgegeben

    for key in keys:    #Für jeden Messwert wird die folgende Schleife ausgeführt
        print(f"\n--- {key} ---")

        sorted_data = merge_sort(data.copy(), key) # Hier wird die Datenliste mit merge sort sortiert

        minimum_item, maximum_item, average = calculate_stats(sorted_data, key) # Hier werden die Minimum, Maximum und Durchschnittswerte berechnet

        print(f"  Minimum: \t{minimum_item[key]}{einheiten[key]} (Datum:{minimum_item['Datum']})") # Diese drei zeilen geben den Minimum, Maximum und Durchschnitt aus und auch noch den Datum 
        print(f"  Maximum: \t{maximum_item[key]}{einheiten[key]} (Datum:{maximum_item['Datum']})")
        print(f"  Durchschnitt: {average:.2f}{einheiten[key]}")

if __name__ == "__main__": # Main wird als erstes ausgeführt
    main()