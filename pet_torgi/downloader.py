import pymupdf
import requests
from pathlib import Path
import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


class DownLoader():
    def __init__(self):
        self.link = None
        self.pdf_path = "data/row/*.pdf"
        self.parket_path = "data/landing/*.parquet" 
        Path("data/row").mkdir(parents=True, exist_ok=True)
        Path("data/landing").mkdir(parents=True, exist_ok=True)

        self.data = None

    def SetLink(self, link, date):
        self.link = link
        date = date.replace(".","-")
        self.pdf_path = self.pdf_path.replace("*", date)
        self.parket_path = self.parket_path.replace("*", date)

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
        
        self.data = pd.concat(dfs, ignore_index=True)

    
    def SaveData(self):
        table = pa.Table.from_pandas(self.data)
        pq.write_table(table, self.parket_path)