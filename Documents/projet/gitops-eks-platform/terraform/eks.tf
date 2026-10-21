module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.8"

  cluster_name    = var.project
  cluster_version = var.cluster_version

  # Endpoint public pour l'acces kubectl/ArgoCD depuis l'exterieur.
  # En production on restreint via cluster_endpoint_public_access_cidrs.
  cluster_endpoint_public_access = true

  # IRSA : permet d'attacher des roles IAM a des ServiceAccounts Kubernetes.
  enable_irsa = true

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  # Donne a l'utilisateur qui applique le Terraform les droits admin sur le cluster.
  enable_cluster_creator_admin_permissions = true

  eks_managed_node_group_defaults = {
    ami_type = "AL2_x86_64"
  }

  eks_managed_node_groups = {
    workers = {
      instance_types = var.node_instance_types
      capacity_type  = "ON_DEMAND"

      min_size     = var.node_min_size
      max_size     = var.node_max_size
      desired_size = var.node_desired_size

      labels = {
        role = "worker"
      }
    }
  }
}
