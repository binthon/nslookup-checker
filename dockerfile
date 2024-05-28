FROM python:3.9-slim

# Ustaw zmienne środowiskowe, aby zapobiec zapisywaniu plików .pyc i zapewnić buforowanie stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Zainstaluj zależności systemowe
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    xvfb \
    x11-apps \
    traceroute \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Zainstaluj geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz && \
    tar -xvzf geckodriver-v0.34.0-linux64.tar.gz && \
    mv geckodriver /usr/local/bin/ && \
    rm geckodriver-v0.34.0-linux64.tar.gz

# Skopiuj plik requirements.txt do katalogu roboczego
COPY requirements.txt /app/

# Zainstaluj zależności Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Skopiuj cały kod aplikacji do katalogu roboczego
COPY . /app/

# Otwórz port 5000 dla zewnętrznych połączeń
EXPOSE 5000

# Ustaw dodatkowe zmienne środowiskowe
ENV NAME World

# Uruchom Xvfb i aplikację
CMD python check-domain.py