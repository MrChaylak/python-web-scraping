from bs4 import BeautifulSoup
# import lxml
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

URL = "https://appbrewery.github.io/Zillow-Clone/"

response = requests.get(URL)

zillow_webpage = response.content

soup = BeautifulSoup(zillow_webpage, "html.parser")

links = soup.select(".StyledPropertyCardDataWrapper a")

links_list = [link.get("href") for link in links]
print(len(links_list))
print(links_list)

prices = soup.select(".PropertyCardWrapper__StyledPriceLine")

prices_list = [price.get_text().split('+')[0].split('/')[0].strip() for price in prices]
print(len(prices_list))
print(prices_list)

addresses = soup.find_all(name="address")

addresses_list = [address.get_text().replace(' |', ',').strip() for address in addresses]
print(len(addresses_list))
print(addresses_list)

#  Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("Form-Link-Here")
driver.maximize_window()

# for i in range(len(addresses_list)):


inputs = [addresses_list, prices_list, links_list]
i = 0
for j in range(len(addresses_list)):
    input_fields = driver.find_elements(By.CSS_SELECTOR, value=".Xb9hP input")
    for field in input_fields:
        field.send_keys(inputs[i][j])
        i += 1
    submit_btn = driver.find_element(By.CLASS_NAME, value="NPEfkd")
    submit_btn.click()
    # time.sleep(0.5)
    new_form_btn = driver.find_element(By.CSS_SELECTOR, value=".c2gzEf a")
    new_form_btn.click()
    # time.sleep(0.5)
    i = 0

#  driver.close()
# driver.quit()
