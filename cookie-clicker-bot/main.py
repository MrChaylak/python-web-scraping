from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def upgrade_checker():
    upgrades_list = driver.find_elements(By.CSS_SELECTOR, "#store div")

    # Find the last non-grayed element
    unlocked_max_upgrade = None
    for upgrade in reversed(upgrades_list):
        if "grayed" not in upgrade.get_attribute("class"):
            unlocked_max_upgrade = upgrade
            break

    # Click on the last non-grayed element if found
    if unlocked_max_upgrade:
        print(unlocked_max_upgrade.text)
        unlocked_max_upgrade.click()
    else:
        print("No available upgrades found.")


#  Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")
driver.maximize_window()

cookie = driver.find_element(By.ID, value="cookie")
timeout = time.time() + 60*5
start_time = time.time()
while True:
    time.sleep(0.1)
    cookie.click()
    if time.time() - start_time > 5:
        start_time = time.time()
        print("check")
        upgrade_checker()
    elif time.time() > timeout:
        print("Exit")
        break
print(driver.find_element(By.ID, value="cps").text)

#  driver.close()
# driver.quit()
