# Analytics lab with Airbyte and Clickhouse

 - Deploy infrastructure with terraform and Yandex Cloud
 - Configure data pipelines with Airbyte

 ## Configure environment

 1. Install devcontainer extension in vscode
 2. Install and start docker
 3. Build container
 > devcontainer build .
 > devcontainer open .

 ### Check terraform and Yandex cloud

 ```
 terraform -v
 yc --version
 ```
### yc init

 ### Deploy infrastructure

  - mv terraformrc .terraformrc
  - cp .env.template .env

### Set environment variables

yc init

```bash
    export YC_TOKEN=$(yc iam create-token)
    export YC_CLOUD_ID=$(yc config get cloud-id)
    export YC_FOLDER_ID=$(yc config get folder-id)
    export TF_VAR_folder_id=$(yc config get folder-id)
    export $(xargs < .env)

  ```

```bash
    terraform init
    terraform validate
    terraform fmt
    terraform plan
    terraform apply
  ``` 

### Login to airbyte yandex_compute_instance_nat_ip_address and port 8000 
airbyte
password

### Connect to SQL SERVER:
yandex_compute_instance_nat_ip_address_sql login: sa passwd:WERTU125

### Connect to Clickhouse:
clickhouse_host_fqdn:8443 db:default user:admin pass:clickhouse

### [CA.pem for yandex](https://cloud.yandex.com/en-ru/docs/managed-clickhouse/operations/connect) 

### Get bucket credentials
```bash
export S3_BUCKET_NAME=$(terraform output -raw yandex_storage_bucket_name)
export S3_ACCESS_KEY=$(terraform output -raw yandex_iam_service_account_static_access_key)
export S3_SECRET_KEY=$(terraform output -raw yandex_iam_service_account_static_secret_key)

echo $S3_BUCKET_NAME
echo $S3_ACCESS_KEY
echo $S3_SECRET_KEY
```
> Set endpoint to storage.yandexcloud.net

> terraform destroy