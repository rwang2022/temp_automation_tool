from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

from drivers.web import WebDriver
from constants import urls
from sources.ihme import IHME

username = "cs.globalhealthimpactproject@gmail.com"
password = "GHI@automat1on"

if __name__ == '__main__':
    ihme = IHME(username, password)
    ihme.select_dropdown_values('estimate', ['Cause of death or injury'])
    ihme.select_dropdown_values('measure', ['DALYs (Disability-Adjusted Life Years)', 'Prevalence'])
    ihme.select_dropdown_values('metric', ['Number','Percent'])
    ihme.select_dropdown_values('cause', ['Lymphatic filariasis'])
    ihme.select_dropdown_values('location', ['Select all countries and territories'])
    ihme.select_dropdown_values('age', ['All ages'])
    ihme.select_dropdown_values('sex', ['Both'])
    ihme.select_dropdown_values('year', ['2015'])
    ihme.download_csv_file(csv_file_name='lf')
