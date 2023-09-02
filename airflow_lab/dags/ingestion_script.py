import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine

from time import time


def ingest_data(table_name,pq_file):
    engine = create_engine(f'postgresql://root:root@de_postgres:5432/ny_taxi')
    parquet_file = pq.ParquetFile(pq_file)

    col_name  = 'airport_fee'
    new_col_name = 'airport_Fee'

    for batch in parquet_file.iter_batches(batch_size = 100000):
        t_start = time()
        
        batch_df = batch.to_pandas()

        if col_name in batch_df.columns:
            batch_df = batch_df.rename(columns={'airport_fee': 'airport_Fee'}, inplace=True)
            print (f'Column {col_name} was renamed to {new_col_name}')
        
        batch_df.to_sql(name=table_name,con=engine, if_exists='append')
        t_end = time()
        print("inserted next chunck.. %.3f seconds" % (t_end - t_start))