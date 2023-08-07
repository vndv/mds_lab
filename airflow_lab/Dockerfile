FROM apache/airflow:2.6.3

ENV AIRFLOW_HOME=/opt/airflow

WORKDIR $AIRFLOW_HOME

USER root
RUN apt-get update

USER airflow
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt