import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
import os
from utils import checker, save_file
from tqdm import tqdm

class Scraper:
    def __init__(self) -> None:
        self.options = Options()
        self.driver = webdriver.Chrome(options=self.options)
        self.by = By
        self.requests = requests
        self.bs = BeautifulSoup
        self.tqdm = tqdm

    def get_haraj_links(
            self,
            url:str, 
            nu_of_pages:int = 5,
            save:bool = False,
            path_or_buf:str = os.getcwd(),
            save_format:str = 'csv',
            mode:str= "w"
            ) -> list:
        """Extract the links of products and/or services from Haraj website

        Parameters
        ========================================
        url: str -> add the url of Haraj.com. You can add the url of any section
            if you need to scrape a specific products or services links.
        nu_of_pages: number of pages that you want to extract links
            data (Number of scrolling). You can either write how many
            scrolls you need to scrape or write None for all links in a
            section or Haraj website.
        save: bool -> If True, the output of the function will be saved
            as file based on the `file_format`. If False, the function will 
            return the output as an object.
            Default : False
        save_format: str -> A file format that is saved when the `save` is 
            True. The accepted format are ["csv", "json", "xlsx", "sql"]
            Default : csv
        save_method: str -> w
            w: write new or overwrite
            a: append
            for more details, refer to Python open function documentation
            
            Returns
            ======================================
            list -> A list of links scraped from Haraj website.
            """
        
        driver = self.driver
        by = self.by
        driver.get(url=url)

        # `load more` XPATH from in Haraj home page.
        load_more = '//*[@id="__next"]/div[2]/div[2]/div/div[2]/div[5]/div/div/button'
        
        # check load_more button.
        try:
            driver.find_element(by.XPATH, load_more).click()
        
        except NoSuchElementException:
            error_message = r"No load more button foud. The posible reason is the developer might changed the XPATH. Try to check first and update the `load_more variable`"
            print(error_message)
            driver.close()
            os._exit(0)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.1)
        
        if nu_of_pages == None:
            while True:
                # Consumes both time and computational resources
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.5)
        else: 
            for i in range(0, nu_of_pages):
                try:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(0.5)
                except TimeoutException as e:
                    print(f"Warrnings: The loading took long time. Check the internert or check the error {e}")

        haraj_links = driver.find_elements(by.CSS_SELECTOR, "a[data-testid='post-title-link']")
        haraj_links = [link.get_attribute("href") for link in haraj_links]
        print(f"{len(haraj_links)} links were scrapped successfully.")

        if save==True:
            save_file(data=haraj_links,
                    path_or_buf=f"{path_or_buf}\\data\\haraj_links.{save_format}", 
                    save_format=save_format,
                    mode=mode,)
            print(f"The `haraj_links.{save_format}` saved to `{path_or_buf}\\data` directory.")
        else:
            return haraj_links



    def get_haraj_details(
                        self,
                        url, 
                        save:bool = False,
                        path_or_buf:str = os.getcwd(), 
                        save_format:str = "csv", 
                        mode:str = "w"
                        ) -> dict:
        """Extract the links from Absher website
        ========================================
        url: str or str list -> add the url
        save: bool -> If True, the output of the function will be saved
            as file based on the `file_format`. If False, the function will 
            return the output as an object.
            Default : False
        save_format: str -> A file format that is saved when the `save` is 
            True. The accepted format are ["csv", "json", "xlsx", "sql"]
            Default : csv
        mode: str -> w
            w: write new or overwrite
            a: append
            for more details, refer to Python open function documentation
            
        Return
        ==========================================
        Dictionary if `save` is Fales
        """
                
        requests = self.requests
        bs = self.bs
        headers = requests.utils.default_headers()
        headers.update({'User-Agent': 'My User Agent 1.0'})

        haraj_data = {
            "ad_title": [],
            "seller": [],
            "city": [],
            "description": [],
            "url": []
        }

        def scrape_data(link):
            try:
                r = requests.get(url=link, headers=headers)
                soup = bs(r.content, features="html5lib")
                body = soup.find(class_="col-span-full md:col-span-3")
                post_header = body.find(class_="flex w-full text-[#525762] dark:text-text-regular rounded-3xl")

                ad_title = post_header.find("h1").contents[0]
                seller_name = post_header.find("a", {"data-testid": "post-author"}).get_text()
                city = post_header.find(class_="city").contents[0]
                desc = body.find("article").get_text().replace("\n", " ")

                haraj_data["ad_title"].append(ad_title)
                haraj_data["seller"].append(seller_name)
                haraj_data["city"].append(city)
                haraj_data["description"].append(desc)
                haraj_data["url"].append(link)

            except Exception as e:
                print(f"{link} was not scrapped because:", e, sep="\n")

        if isinstance(url, str):
            scrape_data(url)
        else:
            tqdm = self.tqdm
            for link in tqdm(url):
                scrape_data(link)

        print(f"{len(haraj_data['ad_title'])} elements were scrapped successfully.")

        if save == False:
            return haraj_data
        else:
            save_file(
                data=haraj_data, 
                path_or_buf=f"{path_or_buf}\\data\\haraj_data.{save_format}", 
                save_format=save_format, 
                mode=mode
                )
            print(haraj_data)
            print(f"The `haraj_data.{save_format}` was saved to `{path_or_buf}\\data` directory.")

    def get_aqar_main(
            self,
            url:str, 
            nu_of_pages:int = 5,
            save:bool = False,
            path_or_buf:str = os.getcwd(),
            save_format:str = 'csv',
            mode:str= "w"
            ) -> list:
        """Extract the main details of properties and/or services from Aqar website

        Parameters
        ========================================
        url: str -> add the url of sa.aqar.fm. You can add the url of any section
            or city if you need to scrape a specific propertie or service ################ADJUST IT.
        nu_of_pages: number of pages that you want to extract ###############ADJUST IT
            data (Pagination). You can either write how many pages
            you need to scrape or write None for all infinite pagination
            in a section or cities in Aqar website.
        save: bool -> If True, the output of the function will be saved
            as file based on the `file_format`. If False, the function will 
            return the output as an object.
            Default : False
        save_format: str -> A file format that is saved when the `save` is 
            True. The accepted format are ["csv", "json", "xlsx", "sql"]
            Default : csv
        save_method: str -> w
            w: write new or overwrite
            a: append
            for more details, refer to Python open function documentation
            
            Returns
            ======================================
            list -> A list of links scraped from Aqar website.
            """
        # check if input is main url format or not. refer to the `checker` function in util
        # to make sure that url=`https:\\sa.aqar.fm\subdirectory` format for pagination purpose.
        url = checker(url=url, aqar_pagination=True)
        #===========================REMOVE LATER=========================
        print("Done, the url is:", url)

        def get_main(url):
            driver = self.driver
            by = self.by

            try:
                driver.get(url=url)
            except WebDriverException as e:
                error_message = rf"Failed to scrape {url} website. I could be internet connection, CloudFlare security or {e}"
                print(error_message)
            
            name = driver.find_elements(by.CSS_SELECTOR, 'div[class="listingCard_top__nVn1L"]')
            price = driver.find_elements(by.CSS_SELECTOR, 'div[class="listingCard_price__N5eJ4"]')
            sblb = driver.find_elements(by.CSS_SELECTOR, 'div[class="listingCard_spec__iKaqt"]') #sblb stands for space - bedroom - livingroom - bathroom
            link = driver.find_elements(by.CSS_SELECTOR, 'div[class="listing_LinkedListingCard__5SRvZ"]')

            #=======================FIX THIS PART======================
            aqar_data = {
            'name':[n.text for n in name], 
            'link':[p.text for p in price],
            'space-br-lr-br':[s.text for s in sblb],
            'link':["https://sa.aqar.fm"+(l.get_attribute('href')) for l in link]
            }

            return aqar_data

        if nu_of_pages==0:
            get_main(url=url)
        else:
            for i in range(0, nu_of_pages):
                tqdm = self.tqdm
                get_main(url=url)
        
        #===========================REMOVE LATER=========================
        print("This website uses CloudFare security. Will fix it ASAP")
        

    def get_aqar_details():
        #===========================REMOVE LATER=========================
        print("This website uses CloudFare security. Will fix it ASAP")

    def get_gatherin_link(
            self,
            url:str, 
            nu_of_pages:int = 10,
            save:bool = False,
            path_or_buf:str = os.getcwd(),
            save_format:str = 'csv',
            mode:str= "w"
            ) -> list:
        pass

    def get_gatherin_details():
        pass

    def get_wasalt_link(
            self,
            url:str, 
            nu_of_pages:int = 10,
            save:bool = False,
            path_or_buf:str = os.getcwd(),
            save_format:str = 'csv',
            mode:str= "w"
            ) -> list:
            pass


    def get_wasalt_details():
        pass

scraper = Scraper()