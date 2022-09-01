import requests
from bs4 import BeautifulSoup

__all__     = ['NotifyElement', 'TnfshNotify']
__version__ = "1.0.0"
__author__  = "tobiichi3227"
# Developed By tobiichi3227

class NotifyElement:
    def __init__(self) -> None:
        self.__text        = ''
        self.__url         = ''
        self.__claim_date  = ''
        self.__claim_group = ''
        self.__is_puttop   = False
        pass

    def getText(self) -> str:
        return self.__text

    def getUrl(self) -> str:
        return self.__url

    def getClaimGroup(self) -> str:
        return self.__claim_group

    def getClaimDate(self) -> str:
        return self.__claim_date

    def getPuttop(self) -> bool:
        return self.__is_puttop

    def setText(self, text: str) -> None:
        self.__text = text

    def setUrl(self, url: str) -> None:
        self.__url = url

    def setClaimGroup(self, claim_group: str) -> None:
        self.__claim_group = claim_group

    def setClaimDate(self, claim_date: str) -> None:
        self.__claim_date = claim_date

    def setPuttop(self, puttop: bool) -> None:
        self.__is_puttop = puttop

class TnfshNotify:
    def __init__(self, url: str) -> None:
        self.__url = url
        self.__html_data = BeautifulSoup(requests.get(self.__url).text, 'html.parser')
        self.__normal_list = []
        self.__puttop_list = []
        self.__gen_notify_data()

    def getNormalList(self):
        return self.__normal_list

    def getPuttopList(self):
        return self.__puttop_list

    # def setNewUrl(self, url: str) -> None:
    #     self.__url = url

    def __gen_notify_data(self) -> None:
        title_list  = self.__html_data.find_all('span', {'class': 'list_word text_le'})

        for title in title_list:
            if title.select('span', {'class': 'puttop'}).__len__() > 0:
                element = NotifyElement()
                element.setUrl(title.select_one('a').get('href'))
                element.setText(title.select_one('a').getText())
                element.setClaimGroup(title.find_next_siblings('span', limit=2)[0].getText())
                element.setClaimDate(title.find_next_siblings('span', limit=2)[1].getText())
                element.setPuttop(True)
                self.__puttop_list.append(element)
            else:
                element = NotifyElement()
                element.setUrl(title.select_one('a').get('href'))
                element.setText(title.select_one('a').getText())
                element.setClaimGroup(title.find_next_siblings('span', limit=2)[0].getText())
                element.setClaimDate(title.find_next_siblings('span', limit=2)[1].getText())
                element.setPuttop(False)
                self.__normal_list.append(element)

    def UpdateNotifyData(self) -> None:
        self.__normal_list.clear()
        self.__puttop_list.clear()
        self.__gen_notify_data()
