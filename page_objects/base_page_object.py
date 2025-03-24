import allure

from ..constants.locators import locators

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class ArtnowPageObject:
    def __init__(self, browser: WebDriver):
        self.browser = browser
        self.browser.get('https://artnow.ru/')

    def find_extra_menu_items_button(self):
        extra_menu_items_button = self.browser.find_element(By.CSS_SELECTOR, locators['button'])
        return extra_menu_items_button
    
    def go_to_menu_item_page(self, link_text='', title_text='', steps=[None, None, None]):
        extra_menu_items_button = self.find_extra_menu_items_button()
        with allure.step(steps[0]):
            assert extra_menu_items_button.value_of_css_property('display') != 'none'
            
            extra_menu_items_button.click()
            with allure.step(steps[1]):
                assert extra_menu_items_button.value_of_css_property('display') == 'none'

        menu_items_list = extra_menu_items_button.parent
        with allure.step(steps[2]):
            menu_items_list.find_element(By.LINK_TEXT, link_text).click()
            assert title_text in self.browser.title

        return self
