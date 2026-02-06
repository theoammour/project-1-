output "bucket_name" {
  description = "Name of the S3 bucket used for the website"
  value       = aws_s3_bucket.portfolio_bucket.id
}

output "website_url" {
  description = "URL of the CloudFront distribution"
  value       = "https://${aws_cloudfront_distribution.s3_distribution.domain_name}"
}
