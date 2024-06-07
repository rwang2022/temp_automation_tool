from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


class WebDriver:

    driver = None

    @staticmethod
    def init():
        if WebDriver.driver is None:
            WebDriver.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    @staticmethod
    def load_url(url):
        WebDriver.driver.get(url)

    @staticmethod
    def find_element_by_id(element_id):
        return WebDriver.driver.find_element(By.ID, element_id)

    @staticmethod
    def find_element_by_class(element_class):
        return WebDriver.driver.find_element(By.CLASS_NAME, element_class)

    @staticmethod
    def find_element_by_xpath(element_xpath):
        return WebDriver.driver.find_element(By.XPATH, element_xpath)

    @staticmethod
    def find_element_by_css_selector(element_css_selector):
        return WebDriver.driver.find_element(By.CSS_SELECTOR, element_css_selector)

    @staticmethod
    def click_on_element(element):
        element.click()

    @staticmethod
    def send_keys_to_element(element, keys):
        element.send_keys(keys)
