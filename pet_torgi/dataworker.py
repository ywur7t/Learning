import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


class DataWorker():
    def __init__(self, path):
        self.data = pq.read_table(path)

    def SaveData(self):
        df = self.data.to_pandas()
        df.to_csv('data.csv')