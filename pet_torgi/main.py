from parser import Parser
from downloader import DownLoader

BASE_LINK = "https://spimex.com"
LINK = f"{BASE_LINK}/markets/oil_products/trades/results/"

if __name__ == "__main__":

    parser = Parser()
    parser.SetLink(LINK).GetPage().GetFileLink()

    print(parser.file_link)

    dlr = DownLoader()
    dlr.SetLink(BASE_LINK+parser.file_link, parser.file_date)
    dlr.GetFile()
    dlr.FindTables()


    print(dlr.data)
    dlr.SaveData()
