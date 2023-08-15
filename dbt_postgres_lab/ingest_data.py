import pandas as pd
import os
import pyarrow.parquet as pq
from sqlalchemy import create_engine
from time import time
from prefect import flow, task
from prefect_sqlalchemy import SqlAlchemyConnector


@task(
    log_prints=True,
    retries=3,
)
def extract_data(url):
    parquet_name = "output.parquet"
    os.system(f"wget {url} -O {parquet_name}")

    return parquet_name


@task(log_prints=True, retries=3)
def ingest_data(parquet_name):
    connection_block = SqlAlchemyConnector.load("postgres-connector")

    with connection_block.get_connection() as engine:
        parquet_file = pq.ParquetFile(parquet_name)

        trips = parquet_file.read().to_pandas()

        trips.head(n=0).to_sql(
            name="yellow_taxi_data", con=engine, if_exists="replace", index=False
        )

        for batch in parquet_file.iter_batches(batch_size=100000):
            t_start = time()
            batch_df = batch.to_pandas()
            batch_df.to_sql(
                name="yellow_taxi_data", con=engine, if_exists="append", index=False
            )
            t_end = time()
            print("inserted next chunck.. %.3f seconds" % (t_end - t_start))


@flow(name="Ingest Flow")
def main_flow():
    url_trip = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-05.parquet"
    raw_data = extract_data(url_trip)
    ingest_data(raw_data)


if __name__ == "__main__":
    main_flow()
