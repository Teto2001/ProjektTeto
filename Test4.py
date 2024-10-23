import openai
import csv
import textwrap

# OpenAI API-Schlüssel setzen
openai.api_key = "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"

def translate_text(text, target_language, max_tokens=1000):
    """Übersetzt einen Text in die Zielsprache, teilt lange Texte in kleinere Stücke."""
    try:
        translated_chunks = []
        # Text in kleinere Abschnitte aufteilen, um das Token-Limit zu berücksichtigen
        chunks = textwrap.wrap(text, width=max_tokens)

        for chunk in chunks:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"Please translate the following text into {target_language}."},
                    {"role": "user", "content": chunk}
                ],
                max_tokens=1000
            )
            translated_chunk = response.choices[0].message['content']
            translated_chunks.append(translated_chunk)

        # Die übersetzten Abschnitte wieder zusammenführen
        return " ".join(translated_chunks)
    except Exception as e:
        print(f"Übersetzungsfehler: {e}")
        return None

def translate_csv(file_path, target_language, output_path):
    """Übersetzt eine CSV-Datei und speichert die Übersetzung."""
    try:
        # Öffnen der CSV-Datei mit der richtigen Kodierung
        with open(file_path, mode='r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            rows = list(reader)

    except UnicodeDecodeError:
        # Fallback auf eine alternative Kodierung, falls utf-8 fehlschlägt
        print("UTF-8-Dekodierung fehlgeschlagen. Versuche ISO-8859-1.")
        with open(file_path, mode='r', encoding='ISO-8859-1') as infile:
            reader = csv.reader(infile)
            rows = list(reader)

    # Kopfzeilen (falls vorhanden) separieren
    headers = rows[0]
    data_rows = rows[1:]

    # Alle Spalten und Zellen übersetzen
    translated_rows = [headers]  # Kopfzeilen in die übersetzte Datei schreiben
    for row in data_rows:
        translated_row = []
        for cell in row:
            translated_cell = translate_text(cell, target_language)
            translated_row.append(translated_cell if translated_cell else cell)
        translated_rows.append(translated_row)

    # Übersetzte Datei speichern
    with open(output_path, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(translated_rows)

    print(f"Übersetzung abgeschlossen. Datei gespeichert unter: {output_path}")

# Beispielaufruf
# Hier sind 50; Mit dieser Code könnte nur 50 Datensätze übersetzt werden
csv_path = r"\\imeso-srv\User\Yolande\Projekt\TeilDaten.csv" # Pfad zur hochgeladenen CSV-Datei
output_fr = "TeilDaten_fr.csv"  # Pfad für die französische Übersetzung
output_en = "TeilDaten_en.csv"  # Pfad für die englische Übersetzung

translate_csv(csv_path, "French", output_fr)  # CSV auf Französisch übersetzen
translate_csv(csv_path, "English", output_en)  # CSV auf Englisch übersetzen