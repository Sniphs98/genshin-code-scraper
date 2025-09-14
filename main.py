import requests
import json
import os

gameName = "Zenless-Zone-Zero"

def getWebsiteText(url):
    """
    Ruft den HTML-Text von der gegebenen URL ab.
    Gibt den Text zurück, falls erfolgreich; andernfalls None.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return None

def getArchivesId(html_text):
    """
    Extrahiert die Archiv-ID aus dem HTML-Text.
    """
    if not html_text:
        return None

    search_word = '>Codes</a>'
    split_list = html_text.split(" ")
    element_list = [text for text in split_list if search_word in text]

    if not element_list:
        print("Der Suchbegriff wurde nicht im HTML-Text gefunden.")
        return None
    try:
        url = element_list[0].split('"')[1]
        url_array = url.split("/")
        number_archives_id = url_array[-1]
        return number_archives_id
    except IndexError:
        print("Konnte die URL oder die ID nicht aus dem gefundenen Element extrahieren.")
        return None

def getCodes(base_url, archives_id):
    """
    Ruft die Webseite mit den Codes ab und extrahiert alle Codes aus dem HTML-Text.
    Gibt eine Liste der Codes zurück.
    """
    if not archives_id:
        print("Keine Archiv-ID übergeben.")
        return None
        
    code_url = f"{base_url}/archives/{archives_id}"
    print(f"Rufe Code-URL ab: {code_url}")
    
    html_text_codes = getWebsiteText(code_url)
    if not html_text_codes:
        print("Fehler beim Abrufen der Codes-Seite.")
        return None
    search_word = "genshin.hoyoverse.com/en/gift?code"
    if gameName == "Zenless-Zone-Zero":
        search_word = "zenless.hoyoverse.com/redemption?code"
    text_array = html_text_codes.split(" ")
    filtered_text_array = [text for text in text_array if search_word in text]
    codes = [text.split("=")[2] for text in filtered_text_array]
    
    return codes

def writeFile(path, web_codes):
    """Schreibt eine Liste von Codes als JSON-Array in eine Datei."""
    with open(path, "w") as f:
        json.dump(web_codes, f, indent=None, separators=(',', ':'))

def readFile(path):
    """Liest Codes aus einer JSON-Datei. Gibt eine leere Liste zurück, wenn die Datei nicht existiert."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r") as f:
            read_codes = json.load(f)
            return read_codes
    except (json.JSONDecodeError, FileNotFoundError):
        return []

# Hauptteil des Programms
print("-------------Start-------------")
url = "https://game8.co/games/" + gameName
path = "code_"+ gameName+".txt"

# 1. Alte Codes aus der Datei lesen (oder eine leere Liste, wenn die Datei nicht existiert)
old_codes = readFile(path)

# 2. Neue Codes von der Webseite abrufen
html_text = getWebsiteText(url)
archives_id = getArchivesId(html_text)

if archives_id:
    print(f"Gefundene Archiv-ID: {archives_id}")
    web_codes = getCodes(url, archives_id)

    if web_codes:
        # 3. Neue Codes finden
        new_codes = list(set(web_codes) - set(old_codes))
        
        if new_codes:
            print("\n🎉 Neue Genshin Impact Codes gefunden:")
            for code in new_codes:
                print(code)
        else:
            print("\nKeine neuen Codes gefunden.")
        
        # 4. Gesamte Liste der Codes in die Datei schreiben (aktualisiert die alte Liste)
        writeFile(path, web_codes)
    else:
        print("Konnte keine Codes auf der Seite finden.")
else:
    print("Konnte keine Archiv-ID finden. Abbruch.")
    
print("\n--------------End-------------")