variable "enabled" { type = bool }
variable "role_name" { type = string }
variable "oidc_provider_arn" { type = string }
variable "oidc_issuer_url" { type = string }
variable "namespace" { type = string }
variable "service_account_name" { type = string }

data "aws_iam_policy_document" "assume_role" {
  count = var.enabled ? 1 : 0

  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [var.oidc_provider_arn]
    }

    condition {
      test     = "StringEquals"
      variable = "${replace(var.oidc_issuer_url, "https://", "")}:sub"
      values   = ["system:serviceaccount:${var.namespace}:${var.service_account_name}"]
    }
  }
}

resource "aws_iam_role" "this" {
  count              = var.enabled ? 1 : 0
  name               = var.role_name
  assume_role_policy = data.aws_iam_policy_document.assume_role[0].json
}

output "role_arn" {
  value = var.enabled ? aws_iam_role.this[0].arn : null
}
