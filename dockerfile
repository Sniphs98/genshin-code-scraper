FROM ubuntu

# Paketlisten aktualisieren und notwendige Abhängigkeiten installieren
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    python3 \
    python3-pip \
    chromium-browser \
    chromium-chromedriver \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Google Chrome hinzufügen
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable


COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

# Umgebungsvariablen für Chromium und ChromeDriver anpassen
ENV CHROME_BIN=/usr/bin/google-chrome \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver

COPY . /app
CMD ["python3", "main.py"]
