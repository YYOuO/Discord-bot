import requests
from bs4 import BeautifulSoup

__all__ = ["NotifyElement", "TnfshNotify"]
__version__ = "1.2.0"
__author__ = "tobiichi3227"
# Developed By tobiichi3227

# convert it into tuple for easier manipulation


class NotifyElement:
    def __init__(self) -> None:
        self.__text = ""
        self.__url = ""
        self.__claim_date = ""
        self.__claim_group = ""
        self.__is_puttop = False

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

    def _setText(self, text: str) -> None:
        self.__text = text

    def _setUrl(self, url: str) -> None:
        self.__url = url

    def _setClaimGroup(self, claim_group: str) -> None:
        self.__claim_group = claim_group

    def _setClaimDate(self, claim_date: str) -> None:
        self.__claim_date = claim_date

    def _setPuttop(self, puttop: bool) -> None:
        self.__is_puttop = puttop


class TnfshNotify:
    def __init__(self, url: str) -> None:
        self.__url = url
        self.__html_data = BeautifulSoup(requests.get(self.__url).text, "html.parser")
        self.__normal_list = []
        self.__puttop_list = []
        self.__search_limit = 0
        self.__gen_notify_data()

    def getNormalList(self):
        return self.__normal_list

    def getPuttopList(self):
        return self.__puttop_list

    def getUrl(self) -> str:
        return self.__url

    def setNewUrl(self, url: str) -> None:
        self.__url = url
        self.__gen_notify_data()

    def getSearchLimit(self) -> int:
        return self.__search_limit

    def setSearchLimit(self, search_limit: int) -> None:
        self.__search_limit = search_limit

    def __gen_notify_data(self) -> None:
        if self.__search_limit == 0:
            title_list = self.__html_data.find_all(
                "span", {"class": "list_word text_le"}
            )
        else:
            title_list = self.__html_data.find_all(
                "span", {"class": "list_word text_le"}, limit=self.__search_limit
            )

        for title in title_list:
            if title.select("span", {"class": "puttop"}).__len__() > 0:
                # element = NotifyElement()
                # element._setUrl(title.select_one('a').get('href'))
                # element._setText(title.select_one('a').getText())
                # element._setClaimGroup(title.find_next_siblings('span', limit=2)[0].getText())
                # element._setClaimDate(title.find_next_siblings('span', limit=2)[1].getText())
                # element._setPuttop(True)
                # self.__puttop_list.append(element)
                element = []
                element.append(title.select_one("a").get("href"))
                element.append(title.select_one("a").getText())
                element.append(title.find_next_siblings("span", limit=2)[0].getText())
                element.append(title.find_next_siblings("span", limit=2)[1].getText())
                element.append(True)
                self.__puttop_list.append(tuple(element))
            else:
                # element = NotifyElement()
                # element._setUrl(title.select_one("a").get("href"))
                # element._setText(title.select_one("a").getText())
                # element._setClaimGroup(
                #     title.find_next_siblings("span", limit=2)[0].getText()
                # )
                # element._setClaimDate(
                #     title.find_next_siblings("span", limit=2)[1].getText()
                # )
                # self.__normal_list.append(element)
                element = []
                element.append(title.select_one("a").get("href"))
                element.append(title.select_one("a").getText())
                element.append(title.find_next_siblings("span", limit=2)[0].getText())
                element.append(title.find_next_siblings("span", limit=2)[1].getText())
                self.__normal_list.append(tuple(element))

    def UpdateNotifyData(self) -> None:
        self.__normal_list.clear()
        self.__puttop_list.clear()
        self.__gen_notify_data()
