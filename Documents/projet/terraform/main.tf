# ------------------------------------------------------------------------------
# PROJET PORTFOLIO - ARCHITECTURE 3-TIERS AWS (FREE TIER)
# ------------------------------------------------------------------------------
# Ce fichier déploie une architecture complète 3-Tiers sur AWS.
# Contraintes respectées :
# - Pas de NAT Gateway (coût).
# - EC2 et RDS dans des sous-réseaux publics (sécurisés par Security Groups).
# - Utilisation de ressources éligibles au Free Tier (t2.micro, db.t3.micro).
# ------------------------------------------------------------------------------

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-west-3" # Paris
}

# ------------------------------------------------------------------------------
# 1. RÉSEAU (VPC & Subnets)
# ------------------------------------------------------------------------------

resource "aws_vpc" "main_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "portfolio-vpc"
  }
}

# Internet Gateway pour l'accès internet (remplace le NAT Gateway)
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main_vpc.id

  tags = {
    Name = "portfolio-igw"
  }
}

# Récupération des AZs disponibles
data "aws_availability_zones" "available" {
  state = "available"
}

# Sous-réseau Public 1
resource "aws_subnet" "public_1" {
  vpc_id                  = aws_vpc.main_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = data.aws_availability_zones.available.names[0]
  map_public_ip_on_launch = true # Indispensable car pas de NAT Gateway

  tags = {
    Name = "portfolio-public-subnet-1"
  }
}

# Sous-réseau Public 2
resource "aws_subnet" "public_2" {
  vpc_id                  = aws_vpc.main_vpc.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = data.aws_availability_zones.available.names[1]
  map_public_ip_on_launch = true

  tags = {
    Name = "portfolio-public-subnet-2"
  }
}

# Table de routage pour l'accès internet direct
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.main_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "portfolio-public-rt"
  }
}

# Association de la RT aux sous-réseaux
resource "aws_route_table_association" "public_assoc_1" {
  subnet_id      = aws_subnet.public_1.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "public_assoc_2" {
  subnet_id      = aws_subnet.public_2.id
  route_table_id = aws_route_table.public_rt.id
}

# ------------------------------------------------------------------------------
# 2. SÉCURITÉ (Security Groups)
# ------------------------------------------------------------------------------

# SG pour l'Application Load Balancer (ALB)
resource "aws_security_group" "alb_sg" {
  name        = "portfolio-alb-sg"
  description = "Allow HTTP inbound"
  vpc_id      = aws_vpc.main_vpc.id

  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "portfolio-alb-sg"
  }
}

# SG pour les instances EC2 (Serveurs Web)
resource "aws_security_group" "ec2_sg" {
  name        = "portfolio-ec2-sg"
  description = "Allow HTTP from ALB and SSH for debug"
  vpc_id      = aws_vpc.main_vpc.id

  # Trafic HTTP accepté UNIQUEMENT depuis l'ALB
  ingress {
    description     = "HTTP from ALB"
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb_sg.id]
  }

  # SSH accepté pour le debug (Attention: ouvert à tous ici, à restreindre en prod)
  ingress {
    description = "SSH for debug"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "portfolio-ec2-sg"
  }
}

# SG pour la base de données RDS
resource "aws_security_group" "rds_sg" {
  name        = "portfolio-rds-sg"
  description = "Allow MySQL from EC2 only"
  vpc_id      = aws_vpc.main_vpc.id

  # Trafic MySQL accepté UNIQUEMENT depuis les EC2
  ingress {
    description     = "MySQL from EC2"
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.ec2_sg.id]
  }

  tags = {
    Name = "portfolio-rds-sg"
  }
}

# ------------------------------------------------------------------------------
# 3. COMPUTE (EC2 & Auto Scaling Group)
# ------------------------------------------------------------------------------

# Recherche de la dernière AMI Amazon Linux 2 (compatible Free Tier)
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# Launch Template pour les instances EC2
resource "aws_launch_template" "web_lt" {
  name_prefix   = "portfolio-web-"
  image_id      = data.aws_ami.amazon_linux_2.id
  instance_type = "t2.micro" # Free Tier

  vpc_security_group_ids = [aws_security_group.ec2_sg.id]

  # Script de démarrage (User Data)
  user_data = base64encode(<<-EOF
              #!/bin/bash
              yum update -y
              amazon-linux-extras install nginx1 -y
              systemctl start nginx
              systemctl enable nginx
              
              # Création de la page index.html
              INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
              echo "<h1>Projet Portfolio - Instance ID: $INSTANCE_ID</h1>" > /usr/share/nginx/html/index.html
              EOF
  )

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "portfolio-web-instance"
    }
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "web_asg" {
  name                = "portfolio-web-asg"
  vpc_zone_identifier = [aws_subnet.public_1.id, aws_subnet.public_2.id]
  target_group_arns   = [aws_lb_target_group.alb_tg.arn]

  launch_template {
    id      = aws_launch_template.web_lt.id
    version = "$Latest"
  }

  min_size         = 1
  max_size         = 2
  desired_capacity = 1 # Pour rester gratuit

  tag {
    key                 = "Name"
    value               = "portfolio-web-asg"
    propagate_at_launch = true
  }
}

# ------------------------------------------------------------------------------
# 4. LOAD BALANCING (ALB)
# ------------------------------------------------------------------------------

resource "aws_lb" "main_alb" {
  name               = "portfolio-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = [aws_subnet.public_1.id, aws_subnet.public_2.id]

  tags = {
    Name = "portfolio-alb"
  }
}

resource "aws_lb_target_group" "alb_tg" {
  name     = "portfolio-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main_vpc.id

  health_check {
    path                = "/"
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

resource "aws_lb_listener" "http_listener" {
  load_balancer_arn = aws_lb.main_alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.alb_tg.arn
  }
}

# ------------------------------------------------------------------------------
# 5. BASE DE DONNÉES (RDS MySQL)
# ------------------------------------------------------------------------------

# Subnet Group pour RDS (doit couvrir au moins 2 AZs)
resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "portfolio-rds-subnet-group"
  subnet_ids = [aws_subnet.public_1.id, aws_subnet.public_2.id] # Subnets Publics

  tags = {
    Name = "portfolio-rds-subnet-group"
  }
}

resource "aws_db_instance" "default" {
  identifier        = "portfolio-db"
  allocated_storage = 10 # 10 Go
  engine            = "mysql"
  engine_version    = "8.0"
  instance_class    = "db.t3.micro" # Free Tier eligible (t3.micro ou t2.micro selon region, t3 est standard)
  
  username             = "adminuser"
  password             = "password123" # A changer impérativement en prod !
  parameter_group_name = "default.mysql8.0"
  
  db_subnet_group_name   = aws_db_subnet_group.rds_subnet_group.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]

  multi_az            = false # Pour économiser
  publicly_accessible = false # Pas besoin d'accès direct depuis internet (sécurité)
  skip_final_snapshot = true  # Pour destruction facile
  
  tags = {
    Name = "portfolio-db"
  }
}

# ------------------------------------------------------------------------------
# 6. OUTPUTS
# ------------------------------------------------------------------------------

output "alb_dns_name" {
  description = "URL DNS du Load Balancer (Site Web)"
  value       = "http://${aws_lb.main_alb.dns_name}"
}
