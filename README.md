<h1 align="center">Théo Ammour — Portfolio Cloud & DevOps</h1>

<p align="center">
  Consultant Cloud · Certifié AWS<br/>
  <em>Infrastructure as Code · Kubernetes · CI/CD · Automatisation sur AWS</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/AWS-FF9900?style=flat&logo=amazon-aws&logoColor=white"/>
  <img src="https://img.shields.io/badge/Terraform-7B42BC?style=flat&logo=terraform&logoColor=white"/>
  <img src="https://img.shields.io/badge/Kubernetes-326CE5?style=flat&logo=kubernetes&logoColor=white"/>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat&logo=github-actions&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-3670A0?style=flat&logo=python&logoColor=white"/>
</p>

---

## 👋 À propos

Consultant cloud certifié **AWS**, avec trois années d'expérience en conseil
technique cloud (apprentissage). Je conçois, automatise
et exploite des infrastructures sur AWS, avec une approche *Infrastructure as
Code* et une culture DevOps : tout est reproductible, versionné et documenté.

Ce dépôt rassemble des projets personnels qui mettent en pratique ces
compétences de bout en bout — de la conception réseau au déploiement continu.

## 🧰 Compétences

| Domaine | Technologies |
|---|---|
| **Cloud** | AWS (VPC, EKS, EC2, Lambda, API Gateway, S3, CloudFront, DynamoDB, RDS, ECR, IAM) |
| **IaC** | Terraform (modules, remote state, bonnes pratiques) |
| **Conteneurs & orchestration** | Docker, Kubernetes, Helm, Kustomize |
| **GitOps & CI/CD** | ArgoCD, GitHub Actions, OIDC, Trivy |
| **Observabilité** | Prometheus, Grafana, CloudWatch |
| **Langages** | Python, Bash, HCL, YAML |

## 📂 Projets

> Tous les projets sont dans le dossier [`Documents/projet/`](Documents/projet).

### ⭐ [GitOps Platform on AWS EKS](Documents/projet/gitops-eks-platform)
Plateforme Kubernetes **production-grade** sur AWS : cluster EKS provisionné en
Terraform, exploité en **GitOps** avec ArgoCD (pattern app-of-apps), CI/CD
GitHub Actions sécurisée (OIDC, scan Trivy, push ECR) et observabilité
Prometheus/Grafana. *Le projet le plus complet du portfolio.*

`Terraform` · `EKS` · `ArgoCD` · `Helm/Kustomize` · `GitHub Actions` · `Prometheus`

### [Serverless API](Documents/projet/serverless-api)
API REST 100 % serverless (API Gateway + Lambda + DynamoDB), déployée en
Terraform avec gestion fine des permissions IAM (*least privilege*) et
facturation à l'usage.

`AWS Lambda` · `API Gateway` · `DynamoDB` · `Terraform`

### [Infrastructure 3-Tier](Documents/projet/terraform)
Architecture web 3-tiers haute disponibilité (VPC multi-AZ, ALB, Auto Scaling
Group EC2, RDS MySQL isolée), optimisée pour le *Free Tier* AWS, avec une
sécurité réseau par couche.

`VPC` · `ALB` · `Auto Scaling` · `RDS` · `Terraform`

### [Cloud Portfolio](Documents/projet/cloud-portfolio)
Site statique distribué mondialement via CloudFront + S3 privé sécurisé par
Origin Access Control (OAC), le tout décrit en Infrastructure as Code.

`S3` · `CloudFront` · `OAC` · `Terraform`

### [DevOps Dashboard](Documents/projet/devops-dashboard)
Application microservices conteneurisée (Flask + Redis + Nginx) orchestrée avec
Docker Compose, illustrant reverse proxy et persistance de données.

`Docker` · `Docker Compose` · `Flask` · `Redis` · `Nginx`

## 📫 Contact

- **GitHub** : [@theoammour](https://github.com/theoammour)

---

<p align="center"><sub>Chaque projet est documenté dans son propre README (architecture, déploiement, coûts et nettoyage).</sub></p>
