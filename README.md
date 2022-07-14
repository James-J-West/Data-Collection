# Data Collection Pipeline

> Create and apply a web scraper class to gather info from a chosen website

## Milestone 1 - Picking the website

Chose the website https://uk.webuy.com/ to gather info from. This was chosen as it is probabl the one thing i am most passionate about, games, and i usnderstandf all the information avaliable. Made sure to check the robots.txt to see if the scraping was allowed by the website

## Milestone 2 - Creating a webscraper class

Used selenium to open a firefox browser and open the desired url. The url opened was https://uk.webuy.com/boxsearch/?superCatId=1 as this allows for all the information that i wanted to be gathered. The ability to scroll, click a button based off a tick and search by text values and others were included in the scraper class. This was my first time using OOP and it was a struggle to get to grips with. Definatley not the best, and takes a while to get the info, but it works. Ill improve it in the future.

```python
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random
import numpy as np
import pandas as pd
```
```python
class scraper():
    
    def __init__(self, pause):
        if __name__ == "__main__":
            #Open Firefox
            self.driver = webdriver.Firefox()
            #Set a standard pause
            self.pause = pause
        else:
            print("Uh Oh It Broke!")

    def open_url(self, url):
        #open the url
        self.driver.get(url)
        time.sleep(self.pause)

    def click_but_by_txt(self, TEXT):
        buts = self.driver.find_elements_by_tag_name("button")
        time.sleep(1)
        #Only click if the text on the button matches the given text
        for i in buts:
            if i.text == TEXT:
                i.click()

    def find_single(self, xpath):
        single = self.driver.find_element_by_xpath(xpath)
        time.sleep(self.pause)
        return single

    def find_multi(self, xpath):
        list_ = self.driver.find_elements_by_xpath(xpath)
        time.sleep(self.pause)
        return list_

    def find_multi_class(self, clas):
        list_ = self.driver.find_elements_by_class_name(clas)
        time.sleep(self.pause)
        return list_



    def scroll_down_all(self):

        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:

            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(5)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                break
            last_height = new_height


    
    def find_single_by_txt(self, TEXT):
        xpath = "//*[contains(text(), '{}')]".format(TEXT)
        single = self.driver.find_element_by_xpath(xpath)
        time.sleep(1)
        return single

    def find_multi_by_txt(self, TEXT):
        xpath = "//*[contains(text(), '{}')]".format(TEXT)
        list_ = self.driver.find_elements_by_xpath(xpath)
        time.sleep(1)
        return list_

        
    def get_links_txt(cont, lst):

        links = []

        for i in lst:
            your_needed_xpath = "//*[contains(text(), '{}')]".format(i)
            for i in cont.find_elements_by_xpath(your_needed_xpath):
                if i.get_attribute("href") != None:
                    print(i.text, i.get_attribute("href"))

                    if i.get_attribute("href") not in links:
                        links.append(i.get_attribute("href"))
        return links
```
## Milestone 3 - Retriving Data From Each Product

Used Selenium to retrieve the name, product id and prices of each product. This was done seperatley for each attribute of the product, in its own method. A UUID was also generated based off the products name, ussing the UUID library. These details were then saved into a dictionary to be extracted into a json file. The image of each product was also collected in its own method.

```python
def get_product_name(self, product, prod_name_class):
        """
        A function which returns the name of a product given the class of the element containing the name

        Parameters:
            product = web element of the product
            prod_name_class = class of the name element
            name_element = web element of the name
        Returns:
            product_name = product name
        """
        name_element = product.find_element_by_class_name(prod_name_class)
        product_name = name_element.text
        return product_name

    def get_product_price(self, product, prod_price_class):
        """
        A function which returns the price of a product given the class of the element containing the price
        
        Parameters:
            product = web element of the product
            prod_price_class = class of the price element
        Returns:
            price = web element of the price
        """
        price = product.find_elements_by_class_name(prod_price_class)

        if len(price) == 1:
            return price[0]
        else:
            return price

    def make_uuid(self, product_name):
        """
        A function which creates and returns a uuid based on the products name
        
        Parameters:
            product_name = name of the product (string)
        Returns:
            uuid_str = generated uuid (String)
        """
        uuid_str = str(uuid.uuid3(uuid.NAMESPACE_DNS, product_name))
        return uuid_str

    def get_prod_id(self, product, product_id_att):
        """
        A function which finds and returns the product id
        
        Parameters:
            product = web element of the product (string)
            product_id_att = attribute of the product id
        Returns:
            id = product id (string)
        """
        id = product.get_attribute(product_id_att)
        return str(id)
        
    def save_screenshots_locally(self, element, folder, filename):
        """
        A function which finds and saves an image for a product given the element containing the image
        
        Parameters:
            element = web element of the image container (WebElement)
            folder = The name of the folder the images will be stored in (string)
            filename = Name of the image we want saves (string)
        Returns:
        """
        element.screenshot(f'.\{folder}\{filename}.png')
```
## Milestone 4 - Testing the methods

Used the unittesting library to create a unit test for each of my methods. These tests open a web page and use each method to retrive information. This information is then compared to the expected result. The test passes or fails based on if the assertion between the expected value and retrieved value is True. I could have made more tests to make the scraper more robust, and maybe use different web pages, but as this was my first time using unittesting, i kept it simple and easy to understand.

```python

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

```
## Milestone 5 - Scalably Storing the data

Created a AWS S3 bucket to store all the raw json files and images in. This was my first time using the s3 bucket and AWS. The tabular data (Prices, names and IDs) were also stored in a RDS using postgres and PgAdmin4. This was tricky as i have never used SQL before, but as i progressed it got easier and easier to manipulate the database. 

## Conclusions

- This project helped me understand that breaking down the project into achievable goals can help understand whats going on and figure out what the next step is and how to do it. To improve, i would move the round timer onto the screen and make it so the camera doesnt close every round
