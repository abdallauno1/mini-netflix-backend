variable "project_name" { description = "Project name prefix" type = string default = "mini-netflix" }
variable "region" { description = "AWS region" type = string default = "eu-central-1" }
variable "instance_type" { description = "EC2 instance type" type = string default = "t3.micro" }
variable "public_key_path" { description = "Path to your SSH public key" type = string default = "~/.ssh/id_rsa.pub" }
