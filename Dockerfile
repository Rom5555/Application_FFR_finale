# Utiliser une image Python officielle
FROM python:3.12

# Mise à jour du système et installation des dépendances nécessaires
RUN apt -y update \
    && apt install -y postgresql \
        apt-utils \
        net-tools \
        postgresql-client \
        libpq-dev \
        tzdata \
        nginx \
    && apt -y upgrade \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les dépendances de l'application et les installer
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le reste du code de l'application
COPY ./ ./

WORKDIR /app/Application_FFR_finale_V1
# Exposer le port sur lequel l'application va tourner
EXPOSE 8000

# Commande pour démarrer l'application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "application_FFR.wsgi:application"]
