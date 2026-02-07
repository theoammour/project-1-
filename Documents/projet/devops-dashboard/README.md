# 🐳 DevOps Dashboard

Un tableau de bord de monitoring simulé, construit avec une architecture **Microservices** conteneurisée.

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=flat&logo=redis&logoColor=white)

## 🏗 Architecture

L'application est composée de 3 conteneurs orchestrés par Docker Compose :

1.  **Web App (Python/Flask)** : Le backend qui génère le tableau de bord HTML.
2.  **Redis** : Base de données en mémoire pour stocker le compteur de vues (persistance des données).
3.  **Nginx** : Reverse Proxy qui sert l'application (Front-Door).

```mermaid
graph LR
    User -->|HTTP :8080| Nginx[Nginx Proxy]
    Nginx -->|Proxy Pass| App[Flask App]
    App -->|Read/Write| Redis[(Redis DB)]
```

## 🚀 Lancer le projet

### Prérequis
*   [Docker Desktop](https://www.docker.com/products/docker-desktop/) installé et lancé.

### Démarrage
1.  Aller dans le dossier :
    ```bash
    cd devops-dashboard
    ```
2.  Lancer les containers :
    ```bash
    docker-compose up --build -d
    ```
3.  Accéder au tableau de bord :
    👉 **http://localhost:8080**

## 🛑 Arrêt
```bash
docker-compose down
```
