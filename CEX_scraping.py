from scraper_object import scraper
import time
import json

#ALL CONSOLES TO SCRAPE
consoles = ["Playstation4 Games"]

#USING THE SCRAPER
cex_scraper = scraper(5)

#CHOICE TO SAVE LOCALLY / UPLOAD
choice_local, choice_upload = cex_scraper.data_choice("cex")
print(choice_local)
print(choice_upload)

#ACCEPt COOKIES
cex_scraper.open_url("https://uk.webuy.com/boxsearch/?superCatId=1")
cex_scraper.click_but_by_txt("Accept Cookies")
time.sleep(4)

#HAVE TO USE BUTTONS TO GET THE LINKS REQUIRED
cex_scraper.click_all_buttons("/html/body/div[1]/div/div/div[6]/div[2]/div[4]/div[2]/ul/li", "a")
web_pages = cex_scraper.get_links_txt(cex_scraper.driver.find_element_by_xpath("/html/body/div[1]/div/div/div[6]/div[2]/div[4]/div[2]/ul"), consoles)

#DETAILS OF ALL RECORDS
all_details = {}


for console_count,web_page in enumerate(web_pages):
    console = consoles[console_count]
    #OPEN URL
    cex_scraper.open_url(web_page)

    #LOAD ALL RESULTS - MAY NEED TO CHANGE AS SOMETIMES DOESNT AUTO LOAD RESULTS
    cex_scraper.scroll_down_all()
    time.sleep(4)

    #GET THE ELEMENT CONTAINING ALL DETAILS
    search_rcrd = cex_scraper.get_products('//div[@class="content-area"]', "searchRcrd")

    for count, record in enumerate(search_rcrd):
        record_id = cex_scraper.get_prod_id(record, "data-insights-object-id")
        record_name = cex_scraper.get_product_name(record, "ais-highlight")
        record_price = cex_scraper.get_product_price(record, "priceTxt")
        record_uuid = cex_scraper.make_uuid(record_name)
        selling_price = record_price[0].text.split(" ")[-1]
        cash_price = record_price[1].text.split(" ")[-1]
        voucher_price = record_price[2].text.split(" ")[-1]
        record_details = [record_uuid,record_id, record_name, selling_price, cash_price, voucher_price]

        #SAVE THE DATA
        filename = f'{record_id}_data.json'
        cex_scraper.save_data(filename, choice_local, choice_upload, [record_uuid, record_id, record_name, selling_price, cash_price, voucher_price], "cex")
        print(f'Record number: {count}')
