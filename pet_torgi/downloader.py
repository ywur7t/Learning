import pymupdf
import requests
from pathlib import Path
import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


class DownLoader():
    def __init__(self, link):
        self.link = link
        self.pdf_path = "./src/output.pdf"
        self.parket_path = "./data/data.parquet"
        Path("./src/").mkdir(parents=True, exist_ok=True)

    def GetFile(self):
        response = requests.get(self.link)
        doc = pymupdf.open(stream=response.content, filetype="pdf")
        doc.save(self.pdf_path)
        doc.close()
        
        

    
        

    def FindTables(self):
        doc = pymupdf.open(self.pdf_path)
        dfs = []
        header = None

        for index, page in enumerate(doc):
            tables = page.find_tables()
            if index == 0:
                tables = tables.tables[3:]

            for table in tables:
                df = table.to_pandas()
                if header is None:
                    header = df.columns.tolist()
                else:
                    df.columns = header

                dfs.append(df)
               
        doc.close()
        if not dfs:
            return None
        
        final_df = pd.concat(dfs, ignore_index=True)
        return pa.Table.from_pandas(final_df)
    
    def SaveData(self, data):
        Path("./data/").mkdir(exist_ok=True)
        pq.write_table(data, self.parket_path)