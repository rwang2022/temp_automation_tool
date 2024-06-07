import time

import requests
import zipfile
from io import BytesIO

from constants import urls
from drivers.web import WebDriver
from selenium.webdriver.common.keys import Keys


class IHME:

    dropdown_fields = {}
    textual_dropdowns = []

    def __init__(self, username, password):
        WebDriver.init()
        WebDriver.load_url(urls.GBD_RESULTS_URL)
        time.sleep(3)
        self.sign_in(username, password)
        self.init_dropdown_references()

    def sign_in(self, username, password):
        sign_in_button = WebDriver.find_element_by_class("ant-btn-default")
        WebDriver.click_on_element(sign_in_button)
        time.sleep(3)
        sign_in_name_field = WebDriver.find_element_by_id("signInName")
        WebDriver.send_keys_to_element(sign_in_name_field, username)
        password_field = WebDriver.find_element_by_id("password")
        WebDriver.send_keys_to_element(password_field, password)
        remember_me_button = WebDriver.find_element_by_id("rememberMe")
        WebDriver.click_on_element(remember_me_button)
        time.sleep(1)
        submit_button = WebDriver.find_element_by_class("fakeSubmitBtn")
        WebDriver.click_on_element(submit_button)
        time.sleep(8)

    def init_dropdown_references(self):
        self.textual_dropdowns = ['cause', 'location']
        self.dropdown_fields = {
            'estimate': WebDriver.find_element_by_xpath(
                "/html/body/vizhub-template/div[2]/div[1]/div/section/div/aside/div/div[2]/div/div[1]/div[2]/div/div/span[1]/input"
            ),
            'measure': WebDriver.find_element_by_xpath(
                "/html/body/vizhub-template/div[2]/div[1]/div/section/div/aside/div/div[2]/div/div[2]/div[2]/div/div/div/div[3]/div/input"
            ),
            'metric': WebDriver.find_element_by_xpath(
                "/html/body/vizhub-template/div[2]/div[1]/div/section/div/aside/div/div[2]/div/div[3]/div[2]/div/div/div/div[4]/div/input"
            ),
            'cause': WebDriver.find_element_by_xpath(
                "/html/body/vizhub-template/div[2]/div[1]/div/section/div/aside/div/div[2]/div/div[4]/div[2]/div/div/div/div[2]/div/input"
            ),
            'location': WebDriver.find_element_by_xpath(
                "/html/body/vizhub-template/div[2]/div[1]/div/section/div/aside/div/div[2]/div/div[5]/div[2]/div/div/div/div[2]/div/input"
            ),
            'age': WebDriver.find_element_by_xpath(
                "/html/body/vizhub-template/div[2]/div[1]/div/section/div/aside/div/div[2]/div/div[6]/div[2]/div/div/div/div[2]/div/input"
            ),
            'sex': WebDriver.find_element_by_xpath(
                "/html/body/vizhub-template/div[2]/div[1]/div/section/div/aside/div/div[2]/div/div[7]/div[2]/div/div/div/div[2]/div/input"
            ),
            'year': WebDriver.find_element_by_xpath(
                "/html/body/vizhub-template/div[2]/div[1]/div/section/div/aside/div/div[2]/div/div[9]/div[2]/div/div/div/div[2]/div/input"
            )
        }

    def select_dropdown_values(self, dropdown_name, selection_list):
        self.reset_dropdown(dropdown_name)
        if dropdown_name in self.textual_dropdowns:
            for selection in selection_list:
                WebDriver.send_keys_to_element(self.dropdown_fields[dropdown_name], Keys.ENTER)
                time.sleep(0.2)
                WebDriver.send_keys_to_element(self.dropdown_fields[dropdown_name], selection)
                time.sleep(0.2)
                WebDriver.send_keys_to_element(self.dropdown_fields[dropdown_name], Keys.ENTER)
                try:
                    dropdown_element = WebDriver.find_element_by_css_selector(f'[aria-label="{selection}, Not selected"]')
                    WebDriver.click_on_element(dropdown_element)
                    time.sleep(0.2)
                except Exception as e:
                    break
                for i in range(len(selection)):
                    WebDriver.send_keys_to_element(self.dropdown_fields[dropdown_name], Keys.BACK_SPACE)
                    time.sleep(0.02)
        else:
            WebDriver.send_keys_to_element(self.dropdown_fields[dropdown_name], Keys.ENTER)
            time.sleep(0.2)
            for selection in selection_list:
                dropdown_element = WebDriver.find_element_by_css_selector(f'[label="{selection}"]')
                WebDriver.click_on_element(dropdown_element)
                time.sleep(0.2)
        WebDriver.send_keys_to_element(self.dropdown_fields[dropdown_name], Keys.ESCAPE)
        time.sleep(1)

    def reset_dropdown(self, dropdown_name):
        for i in range(5):
            WebDriver.send_keys_to_element(self.dropdown_fields[dropdown_name], Keys.BACK_SPACE)
            time.sleep(0.02)

    def download_csv_file(self, csv_file_name):
        dl_button = WebDriver.find_element_by_class("anticon-download")
        WebDriver.click_on_element(dl_button)
        time.sleep(1)
        names_radio = WebDriver.find_element_by_css_selector('[value="names"]')
        WebDriver.click_on_element(names_radio)
        time.sleep(1)
        submit_button = WebDriver.find_element_by_xpath('html/body/div[11]/div/div[2]/div/div[2]/div[3]/button[2]')
        WebDriver.click_on_element(submit_button)
        time.sleep(3)
        sss = WebDriver.find_element_by_xpath('/html/body/div/div/div[2]/div/div[2]/div[2]/div/div/div[2]/span/a')
        sss.send_keys(Keys.LEFT_CONTROL, Keys.ENTER)
        WebDriver.driver.switch_to.window(WebDriver.driver.window_handles[-1])
        time.sleep(1)
        while True:
            try:
                download_button = WebDriver.find_element_by_xpath(
                    "/html/body/vizhub-template/div[2]/div[1]/div[2]/div[3]/div/div[3]/div/div/div/ul/li/div[2]/a"
                )
                break
            except Exception as e:
                pass
        download_link = download_button.get_attribute('href')
        response = requests.get(download_link, allow_redirects=True)
        zip_data = BytesIO(response.content)
        unzipped_data = zipfile.ZipFile(zip_data)
        file_name = ''
        for name in unzipped_data.namelist():
            if name[-4:] == '.csv':
                file_name = name
                break
        csv_file_directory = 'raw_data'
        unzipped_data.getinfo(file_name).filename = csv_file_name + '.csv'
        unzipped_data.extract(file_name, csv_file_directory)

    def close(self):
        WebDriver.driver.close()
