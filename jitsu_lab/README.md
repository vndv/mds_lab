# Jitsu lab

Ingest data from MSSQL and load to Clickhouse with Jitsu

## Configure jitsu
[docker-compose jitsu](https://classic.jitsu.com/docs/deployment/deploy-with-docker/docker-compose)

cd jitsu/docker
docker-compose up -d
http://localhost:8000/configurator 


## Configure dbt
1. install dbt
2. configure dbt_project profiles source

## Configure yandex cloud

`terraform -v

yc --version`

yc init

export YC_TOKEN=$(yc iam create-token)
export YC_CLOUD_ID=$(yc config get cloud-id)
export YC_FOLDER_ID=$(yc config get folder-id)
export $(xargs <.env)

