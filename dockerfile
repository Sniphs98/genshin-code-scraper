FROM ubuntu

# Paketlisten aktualisieren und notwendige Abhängigkeiten installieren
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    wget \
    curl \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt


COPY . /app
CMD ["python3", "main.py"]
