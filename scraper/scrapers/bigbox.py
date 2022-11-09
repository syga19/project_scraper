from scraper.scrapers.base import BaseScraper
from scraper.models.vacuum import Vacuum, VacuumLink

from typing import List, Optional
from bs4 import BeautifulSoup

class BigBox(BaseScraper):
    __items_per_page__: int = 21
    __domain__: str = "https://bigbox.lt"

    def _retrieve_items_list(self, pages_count: int, keyword: str) -> List[VacuumLink]:
        results: List[VacuumLink] = []
        for page_number in range(2, pages_count + 2):
            content = self._get_page_content(f"module/mijorasearch/search?s={keyword}&p={page_number}")
            if content:
                vacuum_list = content.find("ul", class_="product_list")
                if not vacuum_list:
                    break
                all_vacuum_lists = vacuum_list.find_all("div", class_="product-container")
                for vacuum_div in all_vacuum_lists:
                    link_to_vacuum = vacuum_div.find("a")["href"]
                    results.append(VacuumLink(url=link_to_vacuum[25:]))
            else:
                continue
        return results

    def _extract_characteristics(self, content: BeautifulSoup) -> str:
        chr_div = content.find("div", class_="product-page-content")
        chr_table = chr_div.find("table")
        tr_rows = chr_table.find_all("tr")
        characteristics: List[str] = []
        try:
            for tr_row in tr_rows:
                spans = tr_row.find_all("span")
                characteristics.append(f"{spans[0].text.strip()} - {spans[1].text.strip()}")
        except IndexError:
            pass
        return ", ".join(characteristics)

    def _retrieve_vacuum_info(self, link: VacuumLink) -> Optional[Vacuum]:        
        content = self._get_page_content(link.url)
        if content:
            try:
                vacuum_title = content.find("h1", class_="page-heading").find("span").text
                price_vacuum = content.find("span", class_="price").text
            except AttributeError:
                return None

            try:
                main_vacuum_image = (
                    content.find("div", class_="product-gallery").find("span").find("a").find("img").get("src")
                )
            except KeyError:
                main_vacuum_image = None

            return Vacuum(
                title=vacuum_title,
                image_url=main_vacuum_image,
                price=price_vacuum.strip(),
                characteristics=self._extract_characteristics(content),
            )
        else:
            return None