import time
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
from utils import save_file

class Scraper:
    def __init__(self, options):
        # Use lowercase for variable names
        self.options = options()
        self.save_file = save_file()

    def get_haraj_links(
            self, # Add self as the first argument of the method
            url: str, 
            nu_of_pages: int = 10, # Add type annotation for nu_of_pages
            save: bool = False,
            path_or_buf: str = os.getcwd(),
            save_format: str = 'csv',
            mode: str = "w"
            ) -> list: # Add return type annotation
        """Extract the links of products and/or services from Haraj website

        Parameters
        ========================================
        url: str -> add the url of Haraj.com. You can add the url of any section
            if you need to scrape a specific products or services tags.
        nu_of_pages: int -> number of pages that you want to extract links
            data (Number of scrolling). You can either write how many
            scrolls you need to scrape or write None for all links in a
            tags or Haraj website (HPC function and NOT RECOMMENDED for 
            RAM less then 6 GB).
        save: bool -> If True, the output of the function will be saved
            as file based on the `save_format`. If False, the function will 
            return the output as an object.
            Default : False
        save_format: str -> A file format that is saved when the `save` is 
            True. The accepted format are ["csv", "json", "xlsx", "sql"]
            Default : csv
        mode: str -> w
            w: write new or overwrite
            a: append
            for more details, refer to Python open function documentation

        Returns
        ========================================
        list -> A list of links from Haraj website if save is False, otherwise None.
        """
        
        # Use self.options instead of options
        driver = webdriver.Chrome(options=self.options)
        driver.get(url=url)
        
        # Define a constant for the XPATH expression
        LOAD_MORE_BUTTON_XPATH = '//*[@id="__next"]/div[2]/div[2]/div/div[2]/div[5]/div/div/button'
        
        # Use a try-except block to handle NoSuchElementException
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.1)
            
            # Use find_element_by_xpath instead of find_element(By.XPATH)
            driver.find_element_by_xpath(LOAD_MORE_BUTTON_XPATH).click()
            
        except NoSuchElementException:
            print("No load more button found.")
        
        if nu_of_pages == None:
            while True:
                # NOT RECOMMENDED for RAM < 6
                # Consumes both time and computational resources
                
                # Use a try-except block to handle StaleElementReferenceException
                try:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(0.5)
                    
                    # Check if the load more button is still present and clickable
                    load_more_button = driver.find_element_by_xpath(LOAD_MORE_BUTTON_XPATH)
                    if load_more_button.is_displayed() and load_more_button.is_enabled():
                        load_more_button.click()
                    else:
                        break
                    
                except StaleElementReferenceException:
                    print("Load more button is no longer valid.")
                    break
                
        else: 
            for i in range(0, nu_of_pages):
                try:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(0.5)
                    
                    # Check if the load more button is still present and clickable
                    load_more_button = driver.find_element_by_xpath(LOAD_MORE_BUTTON_XPATH)
                    if load_more_button.is_displayed() and load_more_button.is_enabled():
                        load_more_button.click()
                    else:
                        break
                    
                except Exception as e:
                    print(f"Warning: The loading took long time. Check the internet or check the error {e}")
                    break

        haraj_links = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='post-title-link']")
        
        # Use list comprehension instead of for loop to get the href attribute
        haraj_links = [link.get_attribute("href") for link in haraj_links]
        
        print(f"{len(haraj_links)} links were scrapped successfully.")

        if save==True:
            
            # Use os.path.join instead of string concatenation to create file path
            file_path = os.path.join(path_or_buf, "data", f"haraj_links.{save_format}")
            
            save_file(data=haraj_links,
                      path_or_buf=file_path, 
                      save_format=save_format,
                      mode=mode)
            
            print(f"The `haraj_links.{save_format}` saved to `{file_path}`.")
        else:
            return haraj_links