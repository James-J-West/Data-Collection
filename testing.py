from scraper_object import scraper
import unittest

class ProductTestCase(unittest.TestCase):

    def test_click_but_by_text(self):
        driver = scraper(5)
        driver.open_url("https://uk.webuy.com/boxsearch?superCatId=1")
        all_buttons = driver.driver.find_elements_by_tag_name("button")
        text_lst = []
        for i in all_buttons:
            text_lst.append(i.text)
        assert("Accept Cookies" in text_lst)

    def test_get_products(self):
        driver = scraper(5)
        driver.open_url("https://uk.webuy.com/boxsearch?categoryIds=1141")
        driver.click_but_by_txt("Accept Cookies")
        records = driver.get_products('//div[@class="content-area"]', "searchRcrd")
        assert (len(records) == 50)

    def test_get_product_name(self):
        driver = scraper(5)
        driver.open_url("https://uk.webuy.com/boxsearch?categoryIds=1141")
        driver.click_but_by_txt("Accept Cookies")
        records = driver.get_products('//div[@class="content-area"]', "searchRcrd")
        name = driver.get_product_name(records[0], "ais-highlight")
        assert("Spider-Man: Miles Morales (No DLC)" == name)

    def test_get_product_price(self):
        driver = scraper(5)
        driver.open_url("https://uk.webuy.com/boxsearch?categoryIds=1141")
        driver.click_but_by_txt("Accept Cookies")
        records = driver.get_products('//div[@class="content-area"]', "searchRcrd")
        price = driver.get_product_price(records[0], "priceTxt")
        selling = price[0].text.split(" ")[-1]
        assert selling == "£22.00"

    def test_get_prod_id(self):
        driver = scraper(5)
        driver.open_url("https://uk.webuy.com/boxsearch?categoryIds=1141")
        driver.click_but_by_txt("Accept Cookies")
        records = driver.get_products('//div[@class="content-area"]', "searchRcrd")
        id = driver.get_prod_id(records[0], "data-insights-object-id")
        assert str(id) == "711719835929"

unittest.main(argv=[""], verbosity=2, exit=False)
