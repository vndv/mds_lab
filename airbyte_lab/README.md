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

 ### Deploy infrastructure

  - mv terraformrc .terraformrc
  - cp .env.template .env


### [CA.pem for yandex](https://cloud.yandex.com/en-ru/docs/managed-clickhouse/operations/connect) 