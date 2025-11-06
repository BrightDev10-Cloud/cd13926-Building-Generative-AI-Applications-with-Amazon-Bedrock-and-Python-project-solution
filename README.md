# AWS Bedrock Knowledge Base with Aurora Serverless

This project sets up an AWS Bedrock Knowledge Base integrated with an Aurora Serverless PostgreSQL database. It also includes scripts for database setup and file upload to S3.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Project Structure](#project-structure)
4. [Deployment Steps](#deployment-steps)
5. [Using the Scripts](#using-the-scripts)
6. [Customization](#customization)
7. [Troubleshooting](#troubleshooting)

## Project Overview

This project consists of several components:

1. Stack 1 - Terraform configuration for creating:
   - A VPC
   - An Aurora Serverless PostgreSQL cluster
   - s3 Bucket to hold documents
   - Necessary IAM roles and policies

2. Stack 2 - Terraform configuration for creating:
   - A Bedrock Knowledge Base
   - Necessary IAM roles and policies

3. A set of SQL queries to prepare the Postgres database for vector storage
4. A Python script for uploading files to an s3 bucket

The goal is to create a Bedrock Knowledge Base that can leverage data stored in an Aurora Serverless database, with the ability to easily upload supporting documents to S3. This will allow us to ask the LLM for information from the documentation.

## Prerequisites

Before you begin, ensure you have the following:

- AWS CLI installed and configured with appropriate credentials (e.g., via `aws configure` or `aws sso login`). Ensure these credentials have permissions to upload objects to S3.
- Terraform installed (version 0.12 or later)
- Python 3.10 or later
- pip (Python package manager)

## Project Structure

```
project-root/
│
├── stack1
|   ├── main.tf
|   ├── outputs.tf
|   └── variables.tf
|
├── stack2
|   ├── main.tf
|   ├── outputs.tf
|   └── variables.tf
|
├── modules/
│   ├── aurora_serverless/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── bedrock_kb/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
│
├── scripts/
│   ├── aurora_sql.sql
│   └── upload_to_s3.py
│
├── spec-sheets/
│   └── machine_files.pdf
│
└── README.md
```

## Deployment Steps

1. Clone this repository to your local machine.

2. Navigate to the project Stack 1. This stack includes VPC, Aurora servlerless and S3

3. Initialize Terraform:
   ```
   terraform init
   ```

4. Review and modify the Terraform variables in `main.tf` as needed, particularly:
   - AWS region
   - VPC CIDR block
   - Aurora Serverless configuration
   - s3 bucket

5. Deploy the infrastructure:
   ```
   terraform apply
   ```
   Review the planned changes and type "yes" to confirm.

6. After the Terraform deployment is complete, note the outputs, particularly the Aurora cluster endpoint.

7. Prepare the Aurora Postgres database. This is done by running the sql queries in the script/ folder. This can be done through Amazon RDS console and the Query Editor.

8. Navigate to the project Stack 2. This stack includes Bedrock Knowledgebase

9. Initialize Terraform:
   ```
   terraform init
   ```

10. Use the values outputs of the stack 1 to modify the values in `main.tf` as needed:
     - Bedrock Knowledgebase configuration

11. Deploy the infrastructure:
      ```
      terraform apply
      ```
      - Review the planned changes and type "yes" to confirm.


12. Upload pdf files to S3, place your files in the `spec-sheets` folder and run:
      ```
      python scripts/upload_to_s3.py
      ```
      - Make sure to update the S3 bucket name in the script before running.

13. Sync the data source in the knowledgebase to make it available to the LLM.

## Post-Deployment Steps

### 0. Install Python Dependencies

Before running any Python scripts, ensure all necessary dependencies are installed:

```bash
pip install -r requirements.txt
```

Now that your infrastructure is provisioned, follow these steps to prepare your data and run the chat application.

### 1. Prepare and Upload Documents to S3

The `upload_to_s3.py` script uploads your documents to the S3 bucket created by Stack 1, which will then be ingested by the Bedrock Knowledge Base.

1.  **Place Your Documents**: Put all your PDF specification sheets (or other relevant documents) into the `spec-sheets/` folder:
    ```
    project-root/
    └── scripts/
        └── spec-sheets/
            ├── your-document-1.pdf
            └── your-document-2.pdf
    ```
2.  **Update S3 Bucket Name in Script**: Open `scripts/upload_s3.py` and update the `bucket_name` variable with the actual name of the S3 bucket provisioned by Stack 1.
3.  **Run the Upload Script**: Execute the script from your terminal:
    ```bash
    python scripts/upload_s3.py
    ```

### 2. Sync Bedrock Knowledge Base Data Source

After uploading your documents to S3, you need to sync the Bedrock Knowledge Base to ingest them.

1.  **Navigate to Bedrock Console**: Go to the AWS Management Console and search for "Bedrock".
2.  **Select Knowledge Bases**: In the Bedrock console, click on "Knowledge bases" in the left navigation pane.
3.  **Choose Your Knowledge Base**: Select your provisioned knowledge base (e.g., `my-bedrock-kb`).
4.  **Sync Data Source**: Go to the "Data sources" tab, select your data source, and click the "Sync" button. Monitor the status until it shows "Active".

### 3. Run the Chat Application

Once the knowledge base has successfully synced and ingested your documents, you can run the Streamlit chat application.

1.  **Run the App**: Execute the Streamlit application from your terminal:
    ```bash
    streamlit run app.py
    ```
    This will open the chat application in your web browser, allowing you to interact with your Bedrock Knowledge Base.

## Complete chat app

### Complete invoke model and knoweldge base code
- Open the bedrock_utils.py file and the following functions:
  - query_knowledge_base
  - generate_response

### Complete the prompt validation function
- Open the bedrock_utils.py file and the following function:
  - valid_prompt

  Hint: categorize the user prompt

## Troubleshooting

- If you encounter permissions issues, ensure your AWS credentials have the necessary permissions for creating all the resources.
- For database connection issues, check that the security group allows incoming connections on port 5432 from your IP address.
- If S3 uploads fail, verify that your AWS credentials have permission to write to the specified bucket.
- For any Terraform errors, ensure you're using a compatible version and that all module sources are correctly specified.

For more detailed troubleshooting, refer to the error messages and logs provided by Terraform and the Python scripts.