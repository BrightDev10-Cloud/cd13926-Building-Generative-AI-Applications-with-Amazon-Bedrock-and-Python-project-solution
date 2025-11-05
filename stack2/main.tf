terraform {
  backend "s3" {
    bucket         = "my-terraform-project-state-backend"
    key            = "stack2/terraform.tfstate"
    region         = "us-east-1" # CHANGE THIS to the region of your S3 bucket
    dynamodb_table = "my-terraform-lock-table"
  }
}

provider "aws" {
  region = "us-west-2"

  assume_role {
    role_arn = "arn:aws:iam::495613875687:role/TerraformExecutionRole"
  }
}

data "terraform_remote_state" "stack1" {
  backend = "s3"
  config = {
    bucket = "my-terraform-project-state-backend"
    key    = "stack1/terraform.tfstate"
    region = "us-east-1" # Must match the region of the S3 bucket
  }
}

module "bedrock_kb" {
  source = "../modules/bedrock_kb"

  knowledge_base_name        = "my-bedrock-kb"
  knowledge_base_description = "Knowledge base connected to Aurora Serverless database"

  aurora_arn        = data.terraform_remote_state.stack1.outputs.aurora_arn
  aurora_db_name    = "myapp"
  aurora_endpoint   = data.terraform_remote_state.stack1.outputs.aurora_endpoint
  aurora_table_name = "bedrock_integration.bedrock_kb"
  aurora_primary_key_field = "id"
  aurora_metadata_field = "metadata"
  aurora_text_field = "chunks"
  aurora_vector_field = "embedding"
  aurora_username   = "dbadmin"
  aurora_secret_arn = data.terraform_remote_state.stack1.outputs.rds_secret_arn
  s3_bucket_arn = data.terraform_remote_state.stack1.outputs.s3_bucket_name
}