data "aws_iam_policy_document" "lambda-role-policy" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "lambda-role" {
  name               = "c10-games-terraform-pipeline"
  assume_role_policy = data.aws_iam_policy_document.lambda-role-policy.json
}




#STEAM
data "aws_ecr_repository" "lambda-ecr-repo-steam" {
  name = "c10-games-steam-scrape"
}


data "aws_ecr_image" "lambda-image-steam" {
  repository_name = data.aws_ecr_repository.lambda-ecr-repo-steam.name
  image_tag       = "latest"
}

resource "aws_lambda_function" "c10-games-terraform-pipeline-steam" {
    role = aws_iam_role.lambda-role.arn
    function_name = "c10-games-terraform-pipeline-steam"
    package_type = "Image"
    image_uri = data.aws_ecr_image.lambda-image-steam.image_uri
    environment {
        variables = {
          STEAM_BASE_URL = var.STEAM_BASE_URL       
        }
    }
    timeout = 300
}



#GOG
data "aws_ecr_repository" "lambda-ecr-repo-gog" {
  name = "c10-games-gog-scrape"
}


data "aws_ecr_image" "lambda-image-gog" {
  repository_name = data.aws_ecr_repository.lambda-ecr-repo-gog.name
  image_tag       = "latest"
}

resource "aws_lambda_function" "c10-games-terraform-pipeline-gog" {
    role = aws_iam_role.lambda-role.arn
    function_name = "c10-games-terraform-pipeline-gog"
    package_type = "Image"
    image_uri = data.aws_ecr_image.lambda-image-gog.image_uri
    environment {
        variables = {
          GOG_BASE_URL = var.GOG_BASE_URL       
        }
    }
    timeout = 180
}



#EPIC
data "aws_ecr_repository" "lambda-ecr-repo-epic" {
  name = "c10-games-epic-extract"
}


data "aws_ecr_image" "lambda-image-epic" {
  repository_name = data.aws_ecr_repository.lambda-ecr-repo-epic.name
  image_tag       = "latest"
}

resource "aws_lambda_function" "c10-games-terraform-pipeline-epic" {
    role = aws_iam_role.lambda-role.arn
    function_name = "c10-games-terraform-pipeline-epic"
    package_type = "Image"
    image_uri = data.aws_ecr_image.lambda-image-epic.image_uri
    environment {
        variables = {
          EPIC_BASE_URL = var.EPIC_BASE_URL       
        }
    }
    timeout = 180
}


#ALERT
data "aws_ecr_repository" "lambda-ecr-repo-alert" {
  name = "c10-games-daily-alert"
}


data "aws_ecr_image" "lambda-image-alert" {
  repository_name = data.aws_ecr_repository.lambda-ecr-repo-alert.name
  image_tag       = "latest"
}

resource "aws_lambda_function" "c10-games-terraform-alert" {
    role = aws_iam_role.lambda-role.arn
    function_name = "c10-games-terraform-alert"
    package_type = "Image"
    image_uri = data.aws_ecr_image.lambda-image-epic.image_uri
    environment {
        variables = {
        AWS_KEY = var.AWS_KEY,
        AWS_SECRET = var.AWS_SECRET
        }
    }
    timeout = 10
}
