# Utilisez l'image officielle Python comme image de base
FROM python:3.10

# Définit le répertoire de travail
WORKDIR /app

# Copiez les fichiers nécessaires dans le conteneur
COPY . .

# Installez les dépendances requises
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Exécutez l'application
CMD ["python", "./ez_poker/main.py"]
