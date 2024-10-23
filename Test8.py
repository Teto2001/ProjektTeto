import openai
import csv
import tiktoken
from concurrent.futures import ThreadPoolExecutor, as_completed

# OpenAI API-Schlüssel setzen
openai.api_key = "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"

# Initialisieren der Tokenizer-Bibliothek für GPT-4
tokenizer = tiktoken.get_encoding("cl100k_base")

MAX_TOKENS = 2000  # Gesamtzahl an Tokens pro Anfrage, einschließlich der Antwort
BATCH_SIZE = 300  # Anzahl der Zellen, die in einem Batch übersetzt werden

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
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_tokens = token_count
        else:
            current_chunk.append(word)
            current_tokens += token_count

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

    return " ".join(translated_chunks)

def translate_batch(cells, target_language):
    """Übersetzt eine Liste von Zellen als Batch."""
    text = " | ".join(cells)  # Kombiniere die Zellen für eine Batch-Übersetzung
    translation = translate_text(text, target_language)
    return translation.split(" | ")  # Teile die übersetzten Zellen wieder auf

def translate_csv(file_path, target_language, output_path):
    """Übersetzt eine CSV-Datei und speichert die Übersetzung."""
    try:
        with open(file_path, mode='r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            rows = list(reader)
    except UnicodeDecodeError:
        print("UTF-8-Dekodierung fehlgeschlagen. Versuche ISO-8859-1.")
        with open(file_path, mode='r', encoding='ISO-8859-1') as infile:
            reader = csv.reader(infile)
            rows = list(reader)

    headers = rows[0]
    data_rows = rows[1:]
    translated_rows = [headers]

    with ThreadPoolExecutor() as executor:
        futures = []
        for i in range(0, len(data_rows), BATCH_SIZE):
            batch_rows = data_rows[i:i + BATCH_SIZE]
            cells_to_translate = [cell for row in batch_rows for cell in row]
            futures.append(executor.submit(translate_batch, cells_to_translate, target_language))

        for future in as_completed(futures):
            translated_cells = future.result()
            row_start = 0
            for row in data_rows:
                row_length = len(row)
                translated_row = translated_cells[row_start:row_start + row_length]
                translated_rows.append(translated_row)
                row_start += row_length

            print(f"Batch Übersetzung abgeschlossen")

    with open(output_path, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(translated_rows)

    print(f"Übersetzung abgeschlossen. Datei gespeichert unter: {output_path}")

# Beispielaufruf
csv_path = r"\\imeso-srv\User\Yolande\Projekt\TeilDaten400.csv"
output_fr = "TeilDaten400_fr.csv"
output_en = "TeilDaten400_en.csv"

translate_csv(csv_path, "French", output_fr)
translate_csv(csv_path, "English", output_en)
