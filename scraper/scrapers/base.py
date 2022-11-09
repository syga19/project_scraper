from pyparsing import Optional
from scraper.models.vacuum import Vacuum, VacuumLink

from typing import List, Optional
from decimal import DivisionByZero
from abc import ABC, abstractmethod
import math
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

class BaseScraper(ABC):
    __items_per_page__: int = 0
    __domain__: str = ""

    def __init__(self) -> None:
        pass

    @abstractmethod
    def _retrieve_items_list(self, pages_count: int, keyword: str) -> List[VacuumLink]:
        pass

    @abstractmethod
    def _retrieve_vacuum_info(self, link: VacuumLink) -> Optional[Vacuum]:
        pass    

    def _get_page_content(self, query: str) -> Optional[BeautifulSoup]:
        resp = requests.get(f"{self.__domain__}/{query}")
        if resp.status_code == 200:
            return BeautifulSoup(resp.content)
        raise Exception("Cannot reach content")    

    def scrape(self, vacuums_count: int, keyword: str) -> List[Vacuum]:
        try:
            pages_count = math.ceil(vacuums_count / self.__items_per_page__)
        except ZeroDivisionError:
            raise AttributeError("Vacuums per page is set to 0!")
        vacuum_links = self._retrieve_items_list(pages_count, keyword)
        scraped_vacuums: List[Optional[Vacuum]] = []
        for vacuum_link in tqdm(vacuum_links):
            scraped_vacuum = self._retrieve_recipe_info(vacuum_link)
            if scraped_vacuum:
                scraped_vacuums.append(scraped_vacuum)
        return scraped_vacuums
        
