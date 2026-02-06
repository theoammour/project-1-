# Terraform AWS 3-Tier Architecture (Free Tier Friendly)

This project contains a Terraform configuration to deploy a **3-Tier Web Architecture** on AWS. It is designed to be fully compatible with the **AWS Free Tier**, avoiding costly resources like NAT Gateways while maintaining best security practices.

## Architecture Overview

The infrastructure includes:

1.  **Network (VPC)**:
    *   One Custom VPC (`10.0.0.0/16`).
    *   **Internet Gateway** for connectivity (No NAT Gateway used to save costs).
    *   Two **Public Subnets** in different Availability Zones (for High Availability).

2.  **Compute (EC2 & Auto Scaling)**:
    *   **Application Load Balancer (ALB)**: Distributes traffic to web servers.
    *   **Auto Scaling Group (ASG)**: Manages EC2 instances (Min: 1, Max: 2).
    *   **EC2 Instances**: `t2.micro` (Free Tier) running Amazon Linux 2.
    *   **Bootstrap**: Automated installation of Nginx with a custom welcome page.

3.  **Database (RDS)**:
    *   **MySQL Database**: `db.t3.micro` or `db.t2.micro` (Free Tier).
    *   **Security**: Isolated in the VPC, only accessible from the Web Servers (EC2).

## Prerequisites

*   Terraform installed.
*   An **AWS Account** with an Access Key and Secret Key.

## Usage

### 1. Configure Credentials
Set your AWS credentials as environment variables (Recommended) or use `aws configure`.

**PowerShell:**
```powershell
$env:AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY"
$env:AWS_SECRET_ACCESS_KEY="YOUR_SECRET_KEY"
```

### 2. Initialize Terraform
Download the necessary providers.
```bash
terraform init
```

### 3. Plan Deployment
Preview the changes that will be made.
```bash
terraform plan
```

### 4. Deploy Infrastructure
Apply the configuration to create the resources on AWS.
```bash
terraform apply
```
*Type `yes` when prompted.*

### 5. Access the Website
At the end of the deployment, Terraform will output the **DNS URL** of the Load Balancer.
Copy and paste this URL into your browser to see the site.

### 6. Clean Up (Destroy)
To avoid any unexpected charges, destroy the resources when you are done.
```bash
terraform destroy
```

## Security Notes
*   **ALB**: Open to the world (HTTP port 80).
*   **EC2**: Only accept HTTP traffic from the ALB. SSH (port 22) is open for debugging (restrict this in production).
*   **RDS**: Only accepts traffic from EC2 instances. Not accessible from the internet.

## Cost
This architecture is optimized for the **AWS Free Tier**. However, always monitor your AWS Billing Dashboard to ensure you do not exceed usage limits.
