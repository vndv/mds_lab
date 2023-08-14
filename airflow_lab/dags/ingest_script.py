import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine
from tqdm import tqdm

from time import time


def ingest_data(table_name,pq_file):

    trips = pq.read_table(pq_file)
    trips = trips.to_pandas()

    engine = create_engine(f'postgresql://admin:admin@de_postgres:5432/orders')
    trips.head(n=0).to_sql(name=table_name,con=engine, if_exists='replace')
    parquet_file = pq.ParquetFile(pq_file)

    for batch in tqdm(parquet_file.iter_batches(batch_size = 100000)):
        batch_df = batch.to_pandas()
        batch_df.to_sql(name=table_name,con=engine, if_exists='append')