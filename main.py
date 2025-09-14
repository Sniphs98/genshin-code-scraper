import requests

def getWebsiteText(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    except requests.exceptions.RequestException as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

def getArchivesId(html_text):
    """
    Extrahiert die Archiv-ID aus dem HTML-Text, indem es nach einem Link sucht, der '>Codes</a>' enthält.
    Gibt die extrahierte ID zurück oder None, wenn nichts gefunden wird.
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

def getCodes(url, archivesId):
    codeURL = url+"/archives/"+ archivesId
    htmlTextCodes = getWebsiteText(codeURL)
    htmlTextCodes.find()
    return

print("-------------Start-------------")
url = "https://game8.co/games/Genshin-Impact"
htmlText = getWebsiteText(url)
archivesId = getArchivesId(htmlText)
codes = getCodes(url,archivesId)
print(archivesId)
print("--------------End-------------")