from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Edge driver
options = Options()
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)

# URL
url = "https://gathern.co/search?chalet_id=39877&unit_id=67275&srsltid=AfmBOoqBFXZ2_xnvw3YfoNVGAqRKWPG-pzZQYQ1O9ZEH35e1ZbVSBFBT&city=3"

driver.get(url)

# Wait for the element to be present to ensure the page has fully loaded
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-3')))

# Scroll the page to ensure all dynamic content is loaded
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-3')))

# Find the specific div and extract all href attributes from <a> tags within it
div = driver.find_element(By.CSS_SELECTOR, '.MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-3')
links = div.find_elements(By.TAG_NAME, 'a')
for link in links:
    href = link.get_attribute('href')
    print(href)

# Close the WebDriver
driver.quit()