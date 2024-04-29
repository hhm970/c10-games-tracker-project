variable "AWS_SECRET" {
    type = string
}

variable "AWS_KEY" {
    type = string
}

variable "DB_USER" {
    type = string
    default = "postgres"
}

variable "DB_PASSWORD" {
    type = string
}

variable "DB_HOST" {
    type = string
}

variable "DB_NAME" {
    type = string
}

variable "DB_PORT" {
    type = number
}

variable "REGION" {
    type = string
    default = "eu-west-2"
}

variable "GOG_BASE_URL" {
    type = string
}

variable "EPIC_BASE_URL" {
    type = string
}

variable "STEAM_BASE_URL" {
    type = string
}