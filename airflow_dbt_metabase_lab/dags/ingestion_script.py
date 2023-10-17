import pyarrow.parquet as pq
import logging
from sqlalchemy import create_engine
from time import time
from decouple import config


USER=config('PG_USER') 
PASS=config('PG_PASS') 
DB=config('PG_DB') 
PORT=config('PG_PORT') 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ingest_data(table_name, pq_file):
    engine = create_engine(f"postgresql://{USER}:{PASS}@de_postgres:{PORT}/{DB}")
    parquet_file = pq.ParquetFile(pq_file)

    for batch in parquet_file.iter_batches(batch_size=100000):
        t_start = time()
        batch_df = batch.to_pandas()
        batch_df.columns = [c.lower() for c in batch_df.columns]
        batch_df.to_sql(name=table_name, con=engine, if_exists="append",index=False)
        t_end = time()
        logger.info("inserted next chunck.. %.3f seconds" % (t_end - t_start))
        # print("inserted next chunck.. %.3f seconds" % (t_end - t_start))
