terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.40"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.12"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.27"
    }
  }

  # Remote state recommandé en équipe : décommenter et adapter.
  # backend "s3" {
  #   bucket       = "votre-bucket-tfstate"
  #   key          = "gitops-eks-platform/terraform.tfstate"
  #   region       = "eu-west-3"
  #   encrypt      = true
  #   use_lockfile = true
  # }
}
