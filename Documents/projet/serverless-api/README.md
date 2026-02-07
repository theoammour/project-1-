# ⚡ Serverless API (ToDo List)

Une API REST performante et évolutive construite avec une architecture 100% Serverless sur AWS.

![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=flat&logo=terraform&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=flat&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54)

## 🏗 Architecture

```mermaid
graph LR
    User -->|HTTP Request| APIGW[API Gateway]
    APIGW -->|Trigger| Lambda[AWS Lambda\n(Python)]
    Lambda -->|Read/Write| DDB[(DynamoDB Table)]
```

*   **API Gateway** : Point d'entrée HTTP public.
*   **AWS Lambda** : Logique métier (Python 3.9) qui s'exécute à la demande (paie à l'usage).
*   **DynamoDB** : Base de données NoSQL ultra-rapide et scalable.
*   **IAM** : Gestion fine des permissions (Least Privilege).

## 🚀 Déploiement

1.  Aller dans le dossier Terraform :
    ```bash
    cd terraform
    ```
2.  Déployer :
    ```bash
    terraform init
    terraform apply
    ```
3.  Récupérer l'URL de l'API (`api_endpoint`) affichée à la fin.

## 🧪 Tester l'API

Une fois déployée, utilisez `curl` ou Postman.

**Créer une tâche (POST) :**
Remplacez `URL_DE_VOTRE_API` par l'output Terraform.

```bash
curl -X POST -H "Content-Type: application/json" -d '{"task": "Apprendre Terraform"}' URL_DE_VOTRE_API
```

**Lister les tâches (GET) :**

```bash
curl URL_DE_VOTRE_API
```

## 🗑 Nettoyage

```bash
cd terraform
terraform destroy
```
