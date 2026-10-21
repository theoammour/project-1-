# Registre prive pour les images de l'application de demonstration.
resource "aws_ecr_repository" "demo_api" {
  name                 = "${var.project}/demo-api"
  image_tag_mutability = "IMMUTABLE"
  force_delete         = true

  image_scanning_configuration {
    scan_on_push = true
  }
}

# Politique de cycle de vie : on ne garde que les 10 dernieres images
# pour maitriser le cout de stockage du registre.
resource "aws_ecr_lifecycle_policy" "demo_api" {
  repository = aws_ecr_repository.demo_api.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Conserver uniquement les 10 dernieres images"
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = 10
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}
