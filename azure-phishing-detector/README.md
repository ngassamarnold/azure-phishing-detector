# Azure Phishing Detector

Ce projet permet de détecter des signaux de phishing dans les emails en utilisant Microsoft Graph API pour la récupération des messages et Azure AI Language pour l’analyse du contenu.

## Fonctionnalités

- Récupération des emails via Microsoft Graph API
- Analyse automatique du contenu des emails (sentiment, entités sensibles, phrases clés)
- Détection de signaux potentiels de phishing

## Prérequis

- Python 3.8+
- Un compte Azure avec accès à Azure AI Language et Microsoft Graph API
- Les identifiants et clés d’API nécessaires (voir `.env.example`)

## Installation

1. Clonez ce dépôt :
   ```bash
   git clone <url-du-repo>
   cd azure-phishing-detector
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

3. Copiez le fichier `.env.example` en `.env` et renseignez vos variables d’environnement :
   ```
   AZURE_LANGUAGE_ENDPOINT=...
   AZURE_LANGUAGE_KEY=...
   AZURE_CLIENT_ID=...
   AZURE_CLIENT_SECRET=...
   AZURE_TENANT_ID=...
   GRAPH_USER_EMAIL=...
   ```

## Utilisation

Lancez l’analyse des emails :
```bash
python src/main.py
```

Le script affichera pour chaque email :
- Sujet, expéditeur, corps du message
- Résultat d’analyse de sentiment
- Entités sensibles détectées
- Phrases clés extraites

## Structure du projet

- `src/fetch_emails.py` : récupération des emails via Graph API ([src/fetch_emails.py](src/fetch_emails.py))
- `src/analyze_with_azure.py` : analyse du contenu avec Azure AI Language ([src/analyze_with_azure.py](src/analyze_with_azure.py))
- `src/main.py` : script principal ([src/main.py](src/main.py))
- `src/test.py` : exemples et tests manuels ([src/test.py](src/test.py))

## Licence

MIT

