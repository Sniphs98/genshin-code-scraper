# Verwenden des Selenium-Standalone-Chrome-Images als Basis
FROM alpine

# Aktualisiere das System und installiere Python und Pip
USER root
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean

# Setze Python 3 als Standard-Python
RUN ln -s /usr/bin/python3 /usr/bin/python

# Kopiere alle Dateien im aktuellen Verzeichnis in das Arbeitsverzeichnis im Container
COPY . /usr/src/app

# Setze das Arbeitsverzeichnis im Container
WORKDIR /usr/src/app

# Installiere Python-Pakete aus requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Wechsle zurück zum Standardebenennungsbenutzer selenium
USER seluser
