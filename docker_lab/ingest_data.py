import pandas as pd
import os
import pyarrow.parquet as pq
from sqlalchemy import create_engine
from time import time

os.system(f"wget {url_trip}")

parquet_file = pq.ParquetFile('yellow_tripdata_2023-05.parquet')

trips = parquet_file.read().to_pandas()

engine = create_engine('postgresql://root:root@localhost:5433/ny_taxi')

trips.head(n=0).to_sql(name='yellow_taxi_data',con=engine, if_exists='replace',index=False)

for batch in parquet_file.iter_batches(batch_size = 100000):
    t_start = time()
    batch_df = batch.to_pandas()
    batch_df.to_sql(name='yellow_taxi_data',con=engine, if_exists='append',index=False)
    t_end = time()
    print("inserted next chunck.. %.3f seconds" % (t_end - t_start))


