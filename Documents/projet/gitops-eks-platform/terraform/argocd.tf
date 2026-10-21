# --- Installation d'ArgoCD via Helm ---
# ArgoCD est le seul composant installe imperativement par Terraform.
# Tout le reste (apps, monitoring, ingress) est ensuite gere par ArgoCD
# en lisant le depot Git : c'est le principe du "bootstrap" GitOps.
resource "helm_release" "argocd" {
  name             = "argocd"
  namespace        = "argocd"
  create_namespace = true

  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argo-cd"
  version    = "7.3.11"

  # Attendre que tous les pods soient prets evite des erreurs de course
  # lors de la creation de l'application racine juste apres.
  wait    = true
  timeout = 600

  values = [
    yamlencode({
      configs = {
        params = {
          # Demo : on sert l'UI en HTTP (TLS gere en amont par l'ingress).
          "server.insecure" = true
        }
      }
    })
  ]

  depends_on = [module.eks]
}

# --- Application racine (pattern "app-of-apps") ---
# Cette unique Application ArgoCD pointe vers gitops/apps/ dans le depot.
# Chaque fichier de ce dossier est lui-meme une Application : ajouter un
# service en production revient donc a commiter un fichier YAML.
resource "helm_release" "argocd_apps" {
  name      = "argocd-apps"
  namespace = "argocd"

  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argocd-apps"
  version    = "2.0.2"

  values = [
    yamlencode({
      applications = {
        root = {
          namespace = "argocd"
          project   = "default"
          source = {
            repoURL        = var.gitops_repo_url
            targetRevision = var.gitops_target_revision
            path           = "gitops/apps"
          }
          destination = {
            server    = "https://kubernetes.default.svc"
            namespace = "argocd"
          }
          syncPolicy = {
            automated = {
              prune    = true
              selfHeal = true
            }
            syncOptions = ["CreateNamespace=true"]
          }
        }
      }
    })
  ]

  depends_on = [helm_release.argocd]
}
