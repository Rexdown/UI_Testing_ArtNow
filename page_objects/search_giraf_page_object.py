import allure

from .base_page_object import ArtnowPageObject
from ..constants.locators import locators

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
    
class SearchGirafPageObject(ArtnowPageObject):
    def __init__(self, browser: WebDriver):
        super().__init__(browser)

    def print_giraf_in_sarch_and_enter(self):
        with allure.step('Print giraf in sarch and enter'):
            search = self.browser.find_element(By.CSS_SELECTOR, locators['search'])
            if (search):
                search.send_keys("Жираф")

                wait = WebDriverWait(self.browser, 30)
                enter = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, locators['enter_search'])))
                if (enter):
                    enter.click()

        return self
    
    def check_first_paint_after_search(self):
        with allure.step('Check first paint after search'):
            wait = WebDriverWait(self.browser, 30)
            paintings = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, locators['painting_name_in_list'])))

            found_painting = None
            if "Жираф" in paintings[0].text:
                found_painting = paintings[0]

            assert found_painting is not None
            assert "Жираф" in found_painting.text

        return self