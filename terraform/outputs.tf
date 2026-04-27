output "repository_url" {
  value = module.ecr.repository_url
}

output "irsa_role_arn" {
  value = module.iam_irsa.role_arn
}
