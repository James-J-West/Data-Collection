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


## Conclusions

- This project helped me understand that breaking down the project into achievable goals can help understand whats going on and figure out what the next step is and how to do it. To improve, i would move the round timer onto the screen and make it so the camera doesnt close every round
