import os
import selenium
import logging
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import chromedriver_autoinstaller
from dotenv import load_dotenv
from datetime import datetime

# page_objects
from page_objects.result_page import ResultPage

BASEDIR = os.path.dirname(os.path.realpath(__file__))
OUTPUT_DIR = f"{BASEDIR}/output"

# create folders
os.makedirs(OUTPUT_DIR, exist_ok=True)

# log scrape results to file
now = datetime.utcnow().strftime("%Y_%m_%d_%H_%M_%S")
logging.basicConfig(filename=f"{OUTPUT_DIR}/out_{now}.txt",
                    level=logging.INFO,
                    format='%(message)s')

# environment variables
load_dotenv(f"{BASEDIR}/.env")

if os.name == 'nt':
    chromedriver_autoinstaller.install()

chrome_options = Options()
if os.getenv('HEADLESS') == 'True':
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--window-size={}'.format("1920,1080"))
if os.name != 'nt':  # for docker
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(3)
driver.get(os.getenv('FINDING_VANCOUVER_HOMES_URL'))

# search for a city
search_box = driver.find_element_by_class_name("token-input")
search_box.send_keys("Vancouver")
search_box.send_keys(Keys.ENTER)
search_btn = driver.find_element_by_class_name("searchBtn")
search_btn.click()

# search results
result_page = ResultPage(driver)

print("starting scraping")

while True:
    results = result_page.get_results()
    for index in range(len(results)):
        info = result_page.get_result_info(index)
        logging.info(info)

    if not result_page.go_to_next_page():
        break

    # wait for new page to load
    time.sleep(2)

print("finished scraping")