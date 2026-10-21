variable "region" {
  description = "Region AWS cible."
  type        = string
  default     = "eu-west-3" # Paris
}

variable "project" {
  description = "Prefixe de nommage des ressources."
  type        = string
  default     = "gitops-eks"
}

variable "cluster_version" {
  description = "Version de Kubernetes du cluster EKS."
  type        = string
  default     = "1.30"
}

variable "vpc_cidr" {
  description = "Plage CIDR du VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "node_instance_types" {
  description = "Types d'instances du managed node group."
  type        = list(string)
  default     = ["t3.medium"]
}

variable "node_min_size" {
  description = "Nombre minimum de noeuds."
  type        = number
  default     = 2
}

variable "node_max_size" {
  description = "Nombre maximum de noeuds."
  type        = number
  default     = 4
}

variable "node_desired_size" {
  description = "Nombre de noeuds souhaite au demarrage."
  type        = number
  default     = 2
}

variable "gitops_repo_url" {
  description = "URL du depot Git contenant les manifests (app-of-apps)."
  type        = string
  default     = "https://github.com/theoammour/gitops-eks-platform"
}

variable "gitops_target_revision" {
  description = "Branche ou tag suivi par ArgoCD."
  type        = string
  default     = "main"
}

variable "tags" {
  description = "Tags communs appliques a toutes les ressources."
  type        = map(string)
  default = {
    Project   = "gitops-eks-platform"
    ManagedBy = "terraform"
  }
}
