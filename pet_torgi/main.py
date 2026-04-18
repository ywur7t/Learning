from parser import Parser
from downloader import DownLoader
from dataworker import DataWorker

BASE_LINK = "https://spimex.com"
LINK = f"{BASE_LINK}/markets/oil_products/trades/results/"

if __name__ == "__main__":

    parser = Parser()
    parser.SetLink(LINK).GetPage().GetFileLink()

    dlr = DownLoader()
    dlr.SetLink(BASE_LINK+parser.file_link, parser.file_date)
    dlr.GetFile()
    data =  dlr.FindTables()
    dlr.SaveData(data)

    # dw = DataWorker('')
    # dw.SaveData()
