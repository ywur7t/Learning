from parser import Parser
from downloader import DownLoader
from dataworker import DataWorker

BASE_LINK = "https://spimex.com"
LINK = f"{BASE_LINK}/markets/oil_products/trades/results/"

if __name__ == "__main__":
    parser = Parser(LINK)
    parser.GetPage()
    parser.ShowPage()
    element = parser.GetElement("div", "page-content__tabs__block")
    links = parser.GetLinks(element, "a", "pdf")

    dlr = DownLoader(BASE_LINK+links[0])
    dlr.GetFile()
    data =  dlr.FindTables()
    dlr.SaveData(data)

    dw = DataWorker('./data/data1.parquet')
    dw.SaveData()
