import requests
from bs4 import BeautifulSoup


class Parser():
    def __init__(self):
        self.last_date = None        
        self.link = None
        self.status = None
        self.page = None
        self.file_link = None
        self.file_date = None

    def SetLink(self, link):
        self.link = link
        return self
        

    def GetPage(self):
        response = requests.get(self.link)
        if response.status_code == 200:
            self.status = True
            self.page = BeautifulSoup(response.content, 'lxml')
        else:
            self.status = False
            self.page = None
        return self
    

    def ShowPage(self):
        if self.status == True:
            print(self.page.prettify())
            # print(self.page.find(class_="page-content__tabs__block"))
            # print(self.file_link)
            # print(self.file_date)

    def GetFileLink(self):
        parent = "page-content__tabs__block"
        block = self.page.find(class_=parent)

        if block:
            self.file_link = block.find(f'a', href=True).get('href')
            self.file_date = block.find(f'p').find(f'span').text.split()[0]
        
