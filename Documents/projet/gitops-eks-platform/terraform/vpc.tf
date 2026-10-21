locals {
  # On etale le cluster sur 2 AZ pour la haute disponibilite.
  azs = slice(data.aws_availability_zones.available.names, 0, 2)
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.8"

  name = "${var.project}-vpc"
  cidr = var.vpc_cidr

  azs             = local.azs
  private_subnets = [for k, v in local.azs : cidrsubnet(var.vpc_cidr, 4, k)]
  public_subnets  = [for k, v in local.azs : cidrsubnet(var.vpc_cidr, 4, k + 8)]

  # Un seul NAT Gateway (au lieu d'un par AZ) : compromis cout / HA assume
  # pour un environnement de demonstration.
  enable_nat_gateway = true
  single_nat_gateway = true
  enable_dns_hostnames = true

  # Tags requis par EKS pour la decouverte des subnets par les Load Balancers.
  public_subnet_tags = {
    "kubernetes.io/role/elb" = "1"
  }
  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = "1"
  }
}
