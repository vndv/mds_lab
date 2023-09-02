# Airflow lab

> docker-compose build
> 
> docker-compose up airflow-init
>
> docker-compose up -d

UI for airflow localhost:8080

for local work need to activate venv
source venv/bin/activate

pip install apache-airflow==2.6.0

for start check_pg dag need to create connection to database and create pool


after finish work

> docker-compose down