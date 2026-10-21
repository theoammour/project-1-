output "region" {
  description = "Region AWS du deploiement."
  value       = var.region
}

output "cluster_name" {
  description = "Nom du cluster EKS."
  value       = module.eks.cluster_name
}

output "configure_kubectl" {
  description = "Commande pour configurer kubectl sur le cluster."
  value       = "aws eks update-kubeconfig --region ${var.region} --name ${module.eks.cluster_name}"
}

output "ecr_repository_url" {
  description = "URL du depot ECR pour pousser les images."
  value       = aws_ecr_repository.demo_api.repository_url
}

output "argocd_admin_password_cmd" {
  description = "Commande pour recuperer le mot de passe admin initial d'ArgoCD."
  value       = "kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d"
}

output "argocd_port_forward_cmd" {
  description = "Commande pour acceder a l'UI ArgoCD en local."
  value       = "kubectl -n argocd port-forward svc/argocd-server 8080:80"
}
