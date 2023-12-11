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

# USA
USA_all = "https://csrankings.org/#/index?all&us"
## general fields
USA_ai  = "https://csrankings.org/#/index?ai&vision&mlmining&nlp&inforet&us"
USA_sys = "https://csrankings.org/#/index?arch&comm&sec&mod&hpc&mobile&metrics&ops&plan&soft&da&bed&us"
USA_the = "https://csrankings.org/#/index?act&crypt&log&us"
USA_oth = "https://csrankings.org/#/index?graph&chi&robotics&bio&visualization&ecom&us"
## specific fields
USA_arch = "https://csrankings.org/#/index?arch&us"
USA_network = "https://csrankings.org/#/index?comm&us"
USA_database = "https://csrankings.org/#/index?mod&us"
USA_hpc = "https://csrankings.org/#/index?hpc&us"
USA_metr = "https://csrankings.org/#/index?metrics&us"
USA_os = "https://csrankings.org/#/index?ops&us"
USA_proglan = "https://csrankings.org/#/index?plan&us"

# Canada
CND_all = "https://csrankings.org/#/index?all&ca"
## general fields
CND_ai  = "https://csrankings.org/#/index?ai&vision&mlmining&nlp&inforet&ca"
CND_sys = "https://csrankings.org/#/index?arch&comm&sec&mod&hpc&mobile&metrics&ops&plan&soft&da&bed&ca"
CND_the = "https://csrankings.org/#/index?act&crypt&log&ca"
CND_oth = "https://csrankings.org/#/index?graph&chi&robotics&bio&visualization&ecom&ca"
## specific fields
CND_arch = "https://csrankings.org/#/index?arch&ca"
CND_network = "https://csrankings.org/#/index?comm&ca"
CND_database = "https://csrankings.org/#/index?mod&ca"
CND_hpc = "https://csrankings.org/#/index?hpc&ca"
CND_metr = "https://csrankings.org/#/index?metrics&ca"
CND_os = "https://csrankings.org/#/index?ops&ca"
CND_proglan = "https://csrankings.org/#/index?plan&ca"

# world
WORLD_all = "https://csrankings.org/#/index?all&world"
## general fields
WORLD_ai  = "https://csrankings.org/#/index?ai&vision&mlmining&nlp&inforet&world"
WORLD_sys = "https://csrankings.org/#/index?arch&comm&sec&mod&hpc&mobile&metrics&ops&plan&soft&da&bed&world"
WORLD_the = "https://csrankings.org/#/index?act&crypt&log&world"
WORLD_oth = "https://csrankings.org/#/index?graph&chi&robotics&bio&visualization&ecom&world"
## specific fields
WORLD_arch = "https://csrankings.org/#/index?arch&world"
WORLD_network = "https://csrankings.org/#/index?comm&world"
WORLD_database = "https://csrankings.org/#/index?mod&world"
WORLD_hpc = "https://csrankings.org/#/index?hpc&world"
WORLD_metr = "https://csrankings.org/#/index?metrics&world"
WORLD_os = "https://csrankings.org/#/index?ops&world"
WORLD_proglan = "https://csrankings.org/#/index?plan&world"

# Europe
EURO_all = "https://csrankings.org/#/index?all&europe"
## general fields
EURO_ai  = "https://csrankings.org/#/index?ai&vision&mlmining&nlp&inforet&europe"
EURO_sys = "https://csrankings.org/#/index?arch&comm&sec&mod&hpc&mobile&metrics&ops&plan&soft&da&bed&europe"
EURO_the = "https://csrankings.org/#/index?act&crypt&log&europe"
EURO_oth = "https://csrankings.org/#/index?graph&chi&robotics&bio&visualization&ecom&europe"
## specific fields
EURO_arch = "https://csrankings.org/#/index?arch&europe"
EURO_network = "https://csrankings.org/#/index?comm&europe"
EURO_database = "https://csrankings.org/#/index?mod&europe"
EURO_hpc = "https://csrankings.org/#/index?hpc&europe"
EURO_metr = "https://csrankings.org/#/index?metrics&europe"
EURO_os = "https://csrankings.org/#/index?ops&europe"
EURO_proglan = "https://csrankings.org/#/index?plan&europe"


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

