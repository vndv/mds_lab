import pyarrow.parquet as pq
from sqlalchemy import create_engine

from time import time


def ingest_data(table_name, pq_file):
    engine = create_engine(f"postgresql://root:root@de_postgres:5432/ny_taxi")
    parquet_file = pq.ParquetFile(pq_file)

    for batch in parquet_file.iter_batches(batch_size=100000):
        t_start = time()
        batch_df = batch.to_pandas()
        batch_df.columns = [c.lower() for c in batch_df.columns]
        batch_df.to_sql(name=table_name, con=engine, if_exists="append",index=False)
        t_end = time()
        print("inserted next chunck.. %.3f seconds" % (t_end - t_start))
