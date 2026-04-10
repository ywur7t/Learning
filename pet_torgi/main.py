from parser import Parser
from downloader import DownLoader
from dataworker import DataWorker

LINK = "https://spimex.com/markets/oil_products/trades/results/"
BASE_LINK = "https://spimex.com"

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

    dw = DataWorker('./data/data.parquet')
    dw.ShowData()
