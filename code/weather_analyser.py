import csv # Damit man csv Dateien einlesen kann
import os # Damit man Dateipfade finden kann egal wo es liegt

# Hier wird die CSV Datei eingelesen und in einer "Python Liste" gespeichert
def csv_einlesen(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)

    data = [] # Diese Liste wird erstellt wo alle Zeilen von der CSV Datei gespeichert werden. 

    with open(file_path, newline="", encoding="utf-8") as file: # Hier wird die CSV Datei geöffnet
        reader = csv.DictReader(file, delimiter=";")            # Hier wird die CSV Datei Zeile für Zeile eingelesen und in einem Dictionary gespeichert

        for row in reader:  # Hier wird jede Zeile ausgeführt
            data.append({   # Hier werden die Werte von der CSV Datei in die Liste gespeichert. Es wird auch gleich in die richtige Datentypen umgewandelt
                "Datum": row["datum"],
                "Temperatur": float(row["temperatur"]),
                "Windgeschwindigkeit": float(row["windgeschwindigkeit"]),
                "Schneehoehe": float(row["schneehoehe"])
            })

    return data


# Hier wird die Merge Funktion definiert welche zwei sotierte listen bekommt und kombiniert. Es wird key gegeben damit die Funktion weiss welche Dateien benutzt werden sollen
def merge(left, right, key):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i][key] < right[j][key]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


# 🔹 MERGE SORT
def merge_sort(data, key):
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    left = merge_sort(data[:mid], key)
    right = merge_sort(data[mid:], key)

    return merge(left, right, key)

# Hier wird Minimum, Maximum und Durchschnitt berechnet.
def calculate_stats(data, key):
    values = [item[key] for item in data] # Hier werden alle Werte von dem key in einer Liste gespeichert damit man den Durchschnitt berechnen kann

    minimum_item = min(data, key=lambda x: x[key])
    maximum_item = max(data, key=lambda x: x[key])
    average = sum(values) / len(values)

    return minimum_item, maximum_item, average

def header():
    headerline = "=" * 80
    file_path = os.path.abspath(__file__) 
    print(headerline)
    print(" Programmname: WeatherAnalyser – Wetterdaten-Auswertung - Bergbahnen Flumserberg AG, Flums")
    print(" Datei Pfad: " + file_path)
    print(headerline)

header()
data = csv_einlesen("wetterdaten.csv")  # Datei wird geladen
if not data:
    print("Fehler: Keine Daten vorhanden!") # Falls die datei leer ist oder nicht gefunden wird, wird eine Fehlermeldung ausgegeben

keys = ["Temperatur", "Windgeschwindigkeit", "Schneehoehe"] # Die Messwerte werden duchgegangen und die Statistiken werden berechnet und ausgegeben

for key in keys:    #Für jeden Messwert wird die folgende Schleife ausgeführt
    print(f"\n--- {key} ---")

    sorted_data = merge_sort(data.copy(), key) # Hier wird die Datenliste mit merge sort sortiert

    minimum_item, maximum_item, average = calculate_stats(sorted_data, key) # Hier werden die Minimum, Maximum und Durchschnittswerte berechnet

    print(f"  Minimum: \t{minimum_item[key]}\t(Datum: {minimum_item['Datum']})") # Diese beiden zeilen geben den Minimum, Maximum und Durchschnitt aus und auch noch den Datum 
    print(f"  Maximum: \t{maximum_item[key]}\t(Datum: {maximum_item['Datum']})")
    print(f"  Durchschnitt: {average:.2f}")
