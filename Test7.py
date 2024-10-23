import openai
import csv
import time
import tiktoken

# OpenAI API-Schlüssel setzen
openai.api_key = "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"

# Initialisieren der Tokenizer-Bibliothek für GPT-4
tokenizer = tiktoken.get_encoding("cl100k_base")

MAX_TOKENS = 2000  # Gesamtzahl an Tokens pro Anfrage, einschließlich der Antwort

def count_tokens(text):
    """Zählt die Anzahl der Tokens in einem Text."""
    tokens = tokenizer.encode(text)
    return len(tokens)

def split_text_into_chunks(text, max_tokens=MAX_TOKENS - 100):
    """Teilt den Text in kleinere Abschnitte basierend auf der maximalen Token-Anzahl."""
    words = text.split()
    chunks = []
    current_chunk = []

    current_tokens = 0

    for word in words:
        token_count = count_tokens(word)
        if current_tokens + token_count > max_tokens:
            # Wenn das Hinzufügen des nächsten Wortes das Token-Limit überschreitet
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_tokens = token_count
        else:
            current_chunk.append(word)
            current_tokens += token_count

    # Das letzte Chunk hinzufügen
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def translate_text(text, target_language):
    """Übersetzt den Text in die Zielsprache und verarbeitet lange Texte in Chunks."""
    if not text.strip():  # Wenn der Text leer ist, keine Übersetzung durchführen
        return text

    translated_chunks = []
    chunks = split_text_into_chunks(text)

    for chunk in chunks:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"Please translate the following text into {target_language}."},
                    {"role": "user", "content": chunk}
                ],
                max_tokens=MAX_TOKENS
            )
            translated_chunk = response.choices[0].message['content']
            translated_chunks.append(translated_chunk)
        except Exception as e:
            print(f"Übersetzungsfehler: {e}")
            return text  # Falls ein Fehler auftritt, den Originaltext zurückgeben

        # Eine längere Pause zwischen den Anfragen, um Rate-Limits zu vermeiden
        time.sleep(2)

    # Die übersetzten Abschnitte zusammenführen
    return " ".join(translated_chunks)

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
    for i, row in enumerate(data_rows):
        translated_row = []
        for cell in row:
            if cell.strip():  # Nur nicht-leere Zellen übersetzen
                translated_cell = translate_text(cell, target_language)
                translated_row.append(translated_cell if translated_cell else cell)
            else:
                translated_row.append(cell)  # Leere Zellen beibehalten

        translated_rows.append(translated_row)

        # Ausgabe für den Fortschritt
        print(f"Übersetze Zeile {i + 1}/{len(data_rows)} abgeschlossen")

    # Übersetzte Datei speichern
    with open(output_path, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(translated_rows)

    print(f"Übersetzung abgeschlossen. Datei gespeichert unter: {output_path}")

# Beispielaufruf
# Hier sind 300
csv_path = r"\\imeso-srv\User\Yolande\Projekt\TeilDaten300.csv" # Pfad zur hochgeladenen CSV-Datei
output_fr = "TeilDaten300_fr.csv"  # Pfad für die französische Übersetzung
output_en = "TeilDaten300_en.csv"  # Pfad für die englische Übersetzung

translate_csv(csv_path, "French", output_fr)  # CSV auf Französisch übersetzen
translate_csv(csv_path, "English", output_en)  # CSV auf Englisch übersetzen

