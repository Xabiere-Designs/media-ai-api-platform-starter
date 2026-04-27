module "ecr" {
  source          = "./modules/ecr"
  repository_name = var.repository_name
}

module "iam_irsa" {
  source                    = "./modules/iam_irsa"
  enabled                   = var.cluster_oidc_provider_arn != "" && var.cluster_oidc_issuer_url != ""
  role_name                 = "media-ai-irsa-role"
  oidc_provider_arn         = var.cluster_oidc_provider_arn
  oidc_issuer_url           = var.cluster_oidc_issuer_url
  namespace                 = var.namespace
  service_account_name      = var.service_account_name
}
