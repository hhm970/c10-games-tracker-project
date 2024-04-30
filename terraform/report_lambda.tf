data "aws_ecr_repository" "lambda-ecr-repo-weekly-report" {
  name = "c10-games-weekly-report"
}


data "aws_ecr_image" "lambda-image-weekly-report" {
  repository_name = data.aws_ecr_repository.lambda-ecr-repo-load.name
  image_tag       = "latest"
}

resource "aws_lambda_function" "c10-games-terraform-weekly-report" {
    role = aws_iam_role.lambda-role.arn
    function_name = "c10-games-terraform-weekly-report"
    package_type = "Image"
    image_uri = data.aws_ecr_image.lambda-image-load.image_uri
    environment {
        variables = {
        DB_HOST = var.DB_HOST,
        DB_PASSWORD = var.DB_PASSWORD,
        DB_PORT = var.DB_PORT,
        DB_USER = var.DB_USER,
        DB_NAME = var.DB_NAME,
        ACCESS_KEY_ID = var.AWS_KEY,
        SECRET_ACCESS_KEY = var.AWS_SECRET,
        STORAGE_FOLDER = "/tmp"
        }
    }
    timeout = 600
}
