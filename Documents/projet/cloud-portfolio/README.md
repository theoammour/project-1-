# ☁️ Cloud Portfolio

![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=flat&logo=terraform&logoColor=white) ![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=flat&logo=amazon-aws&logoColor=white)

Un portfolio de consultant cloud professionnel, déployé avec une architecture **Serverless** et **Infrastructure as Code**.

## 🏗 Architecture

Le site est hébergé selon les meilleures pratiques de sécurité et de performance AWS :

*   **HTML/CSS/JS** : Site statique léger et rapide.
*   **Amazon S3** : Stockage des fichiers (Accès public bloqué).
*   **Amazon CloudFront** : CDN pour la distribution globale en HTTPS.
*   **Origin Access Control (OAC)** : Sécurisation de l'accès au bucket S3 (seul CloudFront peut lire les fichiers).

```mermaid
graph LR
    User((User)) -->|HTTPS| CF[CloudFront CDN]
    CF -->|OAC Signed Request| S3[S3 Bucket\n(Private)]
```

## 🚀 Guide de Déploiement

### Prérequis
*   [Terraform](https://developer.hashicorp.com/terraform/install) installé.
*   [AWS CLI](https://aws.amazon.com/cli/) configuré (`aws configure`).

### Étape 1 : Déployer l'Infrastructure
1.  Aller dans le dossier Terraform :
    ```bash
    cd terraform
    ```
2.  Initialiser et appliquer :
    ```bash
    terraform init
    terraform apply
    # Tape 'yes' quand demandé
    ```
3.  **Notez les Outputs** à la fin !
    *   `bucket_name` : Le nom de votre bucket S3.
    *   `website_url` : L'URL de votre site.

### Étape 2 : Mettre en ligne le site
Une fois l'infrastructure créée, envoyez les fichiers du site vers le bucket S3.

Remplacez `VOTRE_BUCKET_NAME` par la valeur obtenue à l'étape précédente.

```bash
# Revenir à la racine du projet
cd ..

# Synchroniser le dossier website vers S3
aws s3 sync website/ s3://VOTRE_BUCKET_NAME
```

### Étape 3 : Admirer le résultat
Ouvrez l'URL `website_url` dans votre navigateur. Votre portfolio est en ligne ! 🎉

## 🔄 Mettre à jour le site

Si vous modifiez le code HTML/CSS, relancez simplement la commande de sync :

```bash
aws s3 sync website/ s3://VOTRE_BUCKET_NAME
```
*(Note : CloudFront met en cache les fichiers. Les changements peuvent prendre quelques minutes à apparaître, ou vous pouvez demander une invaladition).*

## 🧹 Nettoyage (Destroy)

Pour tout supprimer et arrêter les (faibles) coûts :

1.  Vider le bucket S3 (Terraform ne peut pas supprimer un bucket plein) :
    ```bash
    aws s3 rm s3://VOTRE_BUCKET_NAME --recursive
    ```
2.  Détruire l'infrastructure :
    ```bash
    cd terraform
    terraform destroy
    ```
