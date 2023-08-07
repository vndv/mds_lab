import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine
from tqdm import tqdm
from time import time

# df = pd.read_parquet('filename.parquet')
# df.to_csv('filename.csv')

trips = pq.read_table('yellow_tripdata_2023-05.parquet')
trips = trips.to_pandas()

# print(pd.io.sql.get_schema(trips,'yellow_taxi_data'))

engine = create_engine('postgresql://imatveev:default@localhost:5432/imatveev')

trips.head(n=0).to_sql(name='yellow_taxi_data',con=engine, if_exists='replace')


# trips.to_sql(name='yellow_taxi_data',con=engine, if_exists='append')

parquet_file = pq.ParquetFile('yellow_tripdata_2023-05.parquet')

for batch in tqdm(parquet_file.iter_batches(batch_size = 100000)):
    batch_df = batch.to_pandas()
    batch_df.to_sql(name='yellow_taxi_data',con=engine, if_exists='append')







