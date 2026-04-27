variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "repository_name" {
  type    = string
  default = "media-ai-api"
}

variable "cluster_oidc_provider_arn" {
  type        = string
  description = "OIDC provider ARN for the EKS cluster"
  default     = ""
}

variable "cluster_oidc_issuer_url" {
  type        = string
  description = "OIDC issuer URL for the EKS cluster"
  default     = ""
}

variable "namespace" {
  type    = string
  default = "default"
}

variable "service_account_name" {
  type    = string
  default = "media-ai-api"
}
