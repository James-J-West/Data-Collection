from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
import time
import uuid
from sqlalchemy import create_engine
import json
import boto3


###########################
#NEED TO UPDATE DOCSTRINGS#
###########################

class scraper():
    
    def __init__(self, pause):
        options = Options()
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')        
        options.add_argument('--no-sandbox')        
        options.add_argument('--headless')        
        options.add_argument("user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        options.headless = True
        self.driver = webdriver.Firefox(options=options)
        self.pause = pause


    def open_url(self, url):
        """
        A function which opens a given url and waits a given amount of time

        Parameters:
            url = url (string)
        Returns:
        """
        self.driver.get(url)
        time.sleep(self.pause)

    def click_but_by_txt(self, TEXT):
        time.sleep(3)
        """
        A function which finds and clicks a button based on the desired text of the button
        
        Parameters:
            TEXT = text of the button to be pressed (string)
        Returns:
        """
        buts = self.driver.find_elements_by_tag_name("button")
        #Only click if the text on the button matches the given text
        for i in buts:
            if i.text == TEXT:
                i.click()
                time.sleep(self.pause)

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

    def scroll_down_all(self):
        """
        A function which will scroll to the bottom of a web page
        
        Parameters:
            new_height = height of the scroll wheel after scrolling
            last_height = height of the scroll wheel before scrolling
        Returns:
        """
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        time.sleep(2)
        while True:
            try:
                element = self.find_single_by_txt("Show more records")
            except NoSuchElementException:
                pass
            try:
                element.click()
            except ElementNotInteractableException:
                pass

            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(5)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")


            if new_height == last_height:
                break
            last_height = new_height
            print("Scrolling")
    
    def find_single_by_txt(self, TEXT):
        """
        A function which finds a single web element if it contains certian text
        
        Parameters:
            TEXT = text of the element (string)
            xpath = xpath of the element formatted with the desired text (string)
        Returns:
            single = Desired single web element
        """
        xpath = "//*[contains(text(), '{}')]".format(TEXT)
        single = self.driver.find_element_by_xpath(xpath)
        return single

    def find_multi_by_txt(self, TEXT):
        """
        A function which finds multiple web elements if they contains certian text
        
        Parameters:
            TEXT = text of the element (string)
            xpath = xpath of the element formatted with the desired text (string)
        Returns:
            list_ = Desired web elements
        """
        xpath = "//*[contains(text(), '{}')]".format(TEXT)
        list_ = self.driver.find_elements_by_xpath(xpath)
        return list_
        
    def get_links_txt(self, cont, lst):
        """
        A function which finds and returns the links of web elements if they contain certian text
        
        Parameters:
            TEXT = text of the button to be pressed (string)
            cont = list of the desired text (list of strings)
            your_needed_xpath = xpath of the element formatted with the desired text (string)
            lst = container of the links
        Returns:
            links = list of desired web links
        """
        links = []
        for i in lst:
            your_needed_xpath = "//*[contains(text(), '{}')]".format(i)
            for i in cont.find_elements_by_xpath(your_needed_xpath):
                if i.get_attribute("href") != None:
                    if i.get_attribute("href") not in links:
                        links.append(i.get_attribute("href"))
        return links

    
    def click_all_buttons(self, button_container_xpath, button_tag):
        """
        A function which finds and clicks all buttons in a web element based on the button tag
        
        Parameters:
            button_container_xpath = xpath of the web element containing the buttons (string)
            button_tag = tag of the button element (string)
            button_container = web element containing the button
            button = the button to be clicked
        Returns:
        """
        button_container = self.driver.find_elements_by_xpath(button_container_xpath)
        for button_element in button_container:
            button = button_element.find_element_by_tag_name(button_tag)
            button.click()
            time.sleep(0.5)

    def get_products(self, product_container_xpath, product_class_name):
        """
        A function returns the list of products using class name
        
        Parameters:
            product_container_xpath = xpath of the element which contains all the products (string)
            product_class_name = class name of the products
            product_container = web element containing the products
        Returns:
            products = list of web element of the products
        """
        product_container = self.driver.find_element_by_xpath(product_container_xpath)
        products = product_container.find_elements_by_class_name(product_class_name)
        return products

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

    def save_data_locally(self, filename, record_details):
        """
        A function to save the data locally
        """
        with open(filename, 'w') as fp:
            json.dump(record_details, fp,  indent=4)

    def data_choice(self, table_name):
        """
        A function to give the user a choice to upload or save the data locally
        """
        locally = int(input("To save data locally - press 1"))
        upload = int(input(f"To upload data to the {table_name} table - press 1"))
        return locally, upload

    def save_data(self,filename,local_choice, upload_choice, record_details, table_name):
        """
        Save the data either locally or upload it using the other methods and based on the users choice
        """

        already_uploaded = self.check_product_id(table_name, record_details[1])

        if local_choice != 1 and upload_choice != 1:
             print("NO DATA WILL BE SAVED")
        elif local_choice == 1 or upload_choice == 1:
            if already_uploaded == False:
                if local_choice == 1 and upload_choice == 1:
                    self.save_data_locally(filename, record_details)
                    self.upload_data_RDS(table_name, record_details[0], record_details[1], record_details[2], record_details[3], record_details[4], record_details[5])
                elif local_choice == 1 and upload_choice != 1:
                    self.save_data_locally(filename, record_details)
                elif local_choice != 1 and upload_choice == 1:
                    self.upload_data_RDS(table_name, record_details[0], record_details[1], record_details[2], record_details[3], record_details[4], record_details[5])
                else:
                    print("NO DATA WILL BE SAVED")

            elif already_uploaded == True:
                print(f"Product with product-id {record_details[1]} has already been uploaded to the table {table_name}")

    def make_data_format(self, uuid, product_id, name, selling, cash, voucher):
        """
        A function to format the data to allow it to be used in the SQL
        """
        name = name.replace("'", "")
        data_formatted = f"('{uuid}', '{product_id}', '{name}', '{selling}', '{cash}', '{voucher}')"
        return data_formatted

    def make_SQL(self, table_name, data):
        """
        A function that crates the SQL Query to upload the data into a table (TABLE HAS TO EXIST ALREADY)
        """
        SQL = f'''INSERT INTO {table_name} VALUES {data}'''
        return SQL

#############################################################
#                                                           #
#                SPECIFIC TO THE CEX_SCRAPING               #
#                                                           #
#############################################################
    
    def upload_data_RDS(self,table_name, uudi, product_id, name, selling, cash, voucher):
        """
        A function that uploads the data to the RDS database server
        """
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        HOST = 'database-1.csoiffuysgtp.eu-west-2.rds.amazonaws.com'
        USER = 'postgres'
        PASSWORD = 'Erzacana_01'
        DATABASE = 'cex--data'
        PORT = 5432
        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
        engine.connect()
        engine.execute(self.make_SQL(table_name, self.make_data_format(uudi, product_id, name, selling, cash, voucher)))

    def check_product_id(self, table_name, product_id):
        """
        A function that uploads the data to the RDS database server
        """
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        HOST = 'database-1.csoiffuysgtp.eu-west-2.rds.amazonaws.com'
        USER = 'postgres'
        PASSWORD = 'Erzacana_01'
        DATABASE = 'cex--data'
        PORT = 5432
        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
        engine.connect()
        uploaded = engine.execute(f"""SELECT product_id FROM {table_name}""").fetchall()
        uploaded_ids = []
        for id_tuple in uploaded:
            uploaded_id = id_tuple[0]
            uploaded_ids.append(uploaded_id)
        if product_id in uploaded_ids:
            return True
        else:
            return False
        
