# Scraping data from Maroof.sa
# This file contains the needed functions to extracts merchandise lists

# Import the required liberaries
from os import link
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager

URL = "https://maroof.sa/BusinessType/BusinessesByTypeList?bid=51&sortProperty=BestRating&DESC=True"

def get_links(url=URL, pagenation=5):
    # instantiate webdriver
    driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    
    # get data from url
    driver.get(url)

    # click on "Load more" button
    # to call all needed data to be crowl
    for i in range(0, pagenation):
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//*[@id="loadMore"]/button').click()

    # extract data from the same website
    links = driver.find_elements(By.CLASS_NAME, "tab-pro-container")
    links = [link.get_attribute("href") for link in links]
    print(f"{len(links)} data was scraped successfully")
    print(links[:5])

##  -------------------------------------