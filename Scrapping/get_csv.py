from bs4 import BeautifulSoup as BS
from selenium.webdriver.common.by import By
import numpy as np
import pandas as pd
import re
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

from utils import bcolors

from utils import USA_all, USA_ai, USA_sys, USA_the, USA_oth, USA_arch, USA_network, USA_database, USA_hpc, USA_metr, USA_os, USA_proglan
from utils import CND_all, CND_ai, CND_sys, CND_the, CND_oth, CND_arch, CND_network, CND_database, CND_hpc, CND_metr, CND_os, CND_proglan
from utils import WORLD_all, WORLD_ai, WORLD_sys, WORLD_the, WORLD_oth, WORLD_arch, WORLD_network, WORLD_database, WORLD_hpc, WORLD_metr, WORLD_os, WORLD_proglan
from utils import EURO_all, EURO_ai, EURO_sys, EURO_the, EURO_oth, EURO_arch, EURO_network, EURO_database, EURO_hpc, EURO_metr, EURO_os, EURO_proglan


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-features=AutomationControlled')


def scrape_university_list(url, country_name):
    """
    @params:url: csranking url with defined filters
    @params:country_name: string; e.g. 'USA', 'CDN', etc.

    @return:university_list: numpy array (1xN)
    """
    # print(bcolors.HEADER+"INFO! start to fetch data from "+url+bcolors.ENDC)
    # service = Service()
    # options = webdriver.ChromeOptions()
    # driver = webdriver.Chrome(service=service, options=options)
    # driver = webdriver.Chrome()
    # driver.get("https://www.google.com")
    
    driver = webdriver.Chrome(executable_path="C:/Program Files/Google/Chrome/Application/chromedriver.exe",
                              options = chrome_options) # necessary to set options, otherwise gets blocked
    
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    time.sleep(2)
    scroll_pause_time = 1
    table_height = 700
    list_height = driver.execute_script("return document.getElementsByClassName('table-responsive')[27].scrollHeight;")
    i = 1

    while True:
        driver.execute_script("document.getElementsByClassName('table-responsive')[27].scrollTo(0, {table_height}*{i});".format(table_height=table_height, i=i))
        i += 1
        time.sleep(scroll_pause_time)
        if i*table_height > list_height:
            break

    soup = BS(driver.page_source, "html.parser")
    driver.quit()
    print(bcolors.OKGREEN+"SUCCESS! fetching data completed successfully"+bcolors.ENDC)

    print(bcolors.HEADER+"INFO! start to scrape institutions of country_field ("+country_name+")"+bcolors.ENDC)
    wait = WebDriverWait(driver, 10)
    # table_content = wait.until(EC.presence_of_element_located((By.ID, "ranking")))
    table_content = soup.find(id="ranking")
    if table_content is not None:
        TDs = table_content.findAll("td")
        university_td = table_content.findAll("span", {"onclick": re.compile(r"csr.*"), "id": False})
        university_list = []
        for i in range(len(university_td)):
            university_list.extend(university_td[i].contents)

        university_list = np.array(university_list, dtype=str)
        # span_hover_td = table_content.findAll("span", {"class": "hovertip", "id": re.compile(r".*-widget"), "title": False})
        # rank = np.array([td.findPrevious().findPrevious().get_text(strip=True) for td in span_hover_td], dtype=int)
        # rank_uni_df = np.concatenate((rank.reshape(rank.shape[0], 1), university_list.reshape(university_list.shape[0], 1)), axis=1)
        # pd.DataFrame(rank_uni_df).to_csv('Institutions_{}.csv'.format(country_name), index = False, header = ['rank','institution'])
        # print(bcolors.OKGREEN+"SUCCESS! Institutions_"+country_name+".csv file is created successfully"+bcolors.ENDC)

        span_hover_td = table_content.findAll("span", {"class": "hovertip", "id": re.compile(r".*-widget"), "title": False})

        data = []
        for td in span_hover_td:
            rank = td.findPrevious().findPrevious().get_text(strip=True)
            university_name = td.findNext().get_text(strip=True)

            # Finding the correct sibling for faculty count (td[3])
            # use debug mode to test the correct sibling
            faculty_count = td.findNext().findNext().findNext().findNext().findNext().findNext().get_text(strip=True)

            # Finding the correct sibling for publication count (td[4])
            # use debug mode as well
            publication_count = td.findNext().findNext().findNext().findNext().findNext().get_text(strip=True)

            data.append([rank, university_name, faculty_count, publication_count])

        # Creating a DataFrame and saving to CSV
        columns = ['Rank', 'University', 'Faculty Count', 'Publication Count']
        df = pd.DataFrame(data, columns=columns)
        df.to_csv('./detailed/Institutions_{}.csv'.format(country_name), index=False)

        print(bcolors.OKGREEN + "SUCCESS! Institutions_{}.csv file is created successfully".format(country_name) + bcolors.ENDC)



if __name__ == "__main__":

    # scrape_university_list(url=WORLD_all, country_name='WORLD_all')
    # general fields
    scrape_university_list(url=WORLD_ai , country_name='WORLD_ai' )
    scrape_university_list(url=WORLD_sys, country_name='WORLD_sys')
    scrape_university_list(url=WORLD_the, country_name='WORLD_the')
    scrape_university_list(url=WORLD_oth, country_name='WORLD_oth')
    # specific fields
    # scrape_university_list(url=WORLD_arch, country_name='WORLD_arch' )
    scrape_university_list(url=WORLD_network, country_name='WORLD_network')
    scrape_university_list(url=WORLD_database, country_name='WORLD_database')
    scrape_university_list(url=WORLD_hpc, country_name='WORLD_hpc')
    scrape_university_list(url=WORLD_metr, country_name='WORLD_metr')
    scrape_university_list(url=WORLD_os, country_name='WORLD_os')
    scrape_university_list(url=WORLD_proglan, country_name='WORLD_proglan')

    scrape_university_list(url=USA_all, country_name='USA_all')
    # general fields
    scrape_university_list(url=USA_ai , country_name='USA_ai' )
    scrape_university_list(url=USA_sys, country_name='USA_sys')
    scrape_university_list(url=USA_the, country_name='USA_the')
    scrape_university_list(url=USA_oth, country_name='USA_oth')
    # specific fields
    scrape_university_list(url=USA_arch, country_name='USA_arch' )
    scrape_university_list(url=USA_network, country_name='USA_network')
    scrape_university_list(url=USA_database, country_name='USA_database')
    scrape_university_list(url=USA_hpc, country_name='USA_hpc')
    scrape_university_list(url=USA_metr, country_name='USA_metr')
    scrape_university_list(url=USA_os, country_name='USA_os')
    scrape_university_list(url=USA_proglan, country_name='USA_proglan')

    scrape_university_list(url=CND_all, country_name='CND_all')
    # general fields
    scrape_university_list(url=CND_ai , country_name='CND_ai' )
    scrape_university_list(url=CND_sys, country_name='CND_sys')
    scrape_university_list(url=CND_the, country_name='CND_the')
    scrape_university_list(url=CND_oth, country_name='CND_oth')
    # specific fields
    scrape_university_list(url=CND_arch, country_name='CND_arch' )
    scrape_university_list(url=CND_network, country_name='CND_network')
    scrape_university_list(url=CND_database, country_name='CND_database')
    scrape_university_list(url=CND_hpc, country_name='CND_hpc')
    scrape_university_list(url=CND_metr, country_name='CND_metr')
    scrape_university_list(url=CND_os, country_name='CND_os')
    scrape_university_list(url=CND_proglan, country_name='CND_proglan')


    scrape_university_list(url=EURO_all, country_name='EURO_all')
    # general fields
    scrape_university_list(url=EURO_ai , country_name='EURO_ai' )
    scrape_university_list(url=EURO_sys, country_name='EURO_sys')
    scrape_university_list(url=EURO_the, country_name='EURO_the')
    scrape_university_list(url=EURO_oth, country_name='EURO_oth')
    # specific fields
    scrape_university_list(url=EURO_arch, country_name='EURO_arch' )
    scrape_university_list(url=EURO_network, country_name='EURO_network')
    scrape_university_list(url=EURO_database, country_name='EURO_database')
    scrape_university_list(url=EURO_hpc, country_name='EURO_hpc')
    scrape_university_list(url=EURO_metr, country_name='EURO_metr')
    scrape_university_list(url=EURO_os, country_name='EURO_os')
    scrape_university_list(url=EURO_proglan, country_name='EURO_proglan')


# scrape_university_list(url=EURO_all, country_name='EURO_all')