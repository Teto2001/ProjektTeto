import openai

# OpenAI API-Key
openai.api_key = "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"

def translate_text(text, target_language):
    try:
        # Erstellen einer Anfrage an ChatGPT, um den Text zu übersetzen
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Modellwahl, du kannst auch "gpt-3.5-turbo" verwenden
            messages=[
                {"role": "system", "content": f"Please translate the following text into {target_language}."},
                {"role": "user", "content": text}
            ],
            max_tokens=1000  # maximale Tokenanzahl für die Antwort
        )
        # Die Antwort von ChatGPT extrahieren
        translated_text = response.choices[0].message['content']
        return translated_text
    except Exception as e:
        print(f"Übersetzungsfehler: {e}")
        return None

# Beispielaufruf
original_text = "Der Patient zeigt Anzeichen einer akuten Myokarditis und hat Kopfschmerzen."
french_translation = translate_text(original_text, "French")
english_translation = translate_text(original_text, "English")

print(f"Original: {original_text}")
print(f"Französisch: {french_translation}")

print(f"Englisch: {english_translation}")
