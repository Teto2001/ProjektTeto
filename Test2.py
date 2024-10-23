import openai

# OpenAI API-Key aus der Umgebungsvariablen abrufen
openai.api_key = "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"

def translate_text(text, target_language):
    """Übersetzt einen Text in die Zielsprache mit der OpenAI API."""
    try:
        # ChatGPT-Anfrage zur Übersetzung des Textes
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"Please translate the following text into {target_language}."},
                {"role": "user", "content": text}
            ],
            max_tokens=1000  # Maximale Tokenanzahl für die Antwort
        )
        # Extrahiere den übersetzten Text
        translated_text = response.choices[0].message['content']
        return translated_text
    except Exception as e:
        print(f"Übersetzungsfehler: {e}")
        return None

def translate_manual(file_path, target_language, output_path):
    """Übersetzt ein Benutzerhandbuch und speichert die Übersetzung mit der OpenAI API."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            manual_content = f.read()

        # Das Handbuch in kleinere Abschnitte aufteilen
        paragraphs = manual_content.split("\n\n")  # Abschnittstrennung nach Absätzen
        translated_paragraphs = []

        # Absätze einzeln übersetzen und Formatierung beibehalten
        for paragraph in paragraphs:
            translated_paragraph = translate_text(paragraph, target_language)
            if translated_paragraph:
                translated_paragraphs.append(translated_paragraph)
            else:
                translated_paragraphs.append(f"Übersetzungsfehler im Abschnitt: {paragraph[:30]}...")

        # Zusammenführen der übersetzten Absätze
        translated_content = "\n\n".join(translated_paragraphs)

        # Übersetzte Datei speichern
        with open(output_path, "w", encoding="utf-8") as f_out:
            f_out.write(translated_content)

        print(f"Übersetzung abgeschlossen. Datei gespeichert unter: {output_path}")
    except FileNotFoundError:
        print(f"Datei nicht gefunden: {file_path}")
    except Exception as e:
        print(f"Fehler bei der Übersetzung des Handbuchs: {e}")

def log_translation_errors(errors, log_file="translation_errors.log"):
    """Schreibt Übersetzungsfehler in eine Log-Datei."""
    try:
        with open(log_file, "a", encoding="utf-8") as log:
            for error in errors:
                log.write(f"{error}\n")
        print(f"Übersetzungsfehler im Log gespeichert: {log_file}")
    except Exception as e:
        print(f"Fehler beim Schreiben der Log-Datei: {e}")

# Beispielaufruf
manual_path = r"\\imeso-srv\User\Yolande\Projekt\Benutzerhanbuch.txt"  # Verwende Raw String für den Dateipfad
output_fr = "benutzerhandbuch_fr.txt"  # Pfad für die französische Übersetzung
output_en = "benutzerhandbuch_en.txt"  # Pfad für die englische Übersetzung

print(f"Versuche, Datei zu öffnen: {manual_path}")

translate_manual(manual_path, "French", output_fr)  # Benutzerhandbuch auf Französisch
translate_manual(manual_path, "English", output_en)  # Benutzerhandbuch auf Englisch
