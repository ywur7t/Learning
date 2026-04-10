import requests
from bs4 import BeautifulSoup


class Parser():
    def __init__(self, link):
        self.last_date = None
        
        self.link = link
        self.status = None
        self.page = None


    def GetPage(self):
        response = requests.get(self.link)
        if response.status_code == 200:
            self.status = True
            self.page = response.content
        else:
            self.status = False
            self.page = None


    def ShowPage(self):
        if self.status == True:
            self.page = BeautifulSoup(self.page, 'lxml')
            return self.page.prettify()
    
    def GetElement(self, value, value1):
        return self.page.find_all(value, value1)
    
    def GetLinks(self, element, value, value1):
        return [link.get("href") for tree in element for link in tree.find_all(value, value1) ]