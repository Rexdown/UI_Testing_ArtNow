import allure

from .base_page_object import ArtnowPageObject
from ..constants.locators import locators

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
    
class PutJewelryPaintingToCartPageObject(ArtnowPageObject):
    def __init__(self, browser: WebDriver):
        super().__init__(browser)
    
    cart_paint_name = '',
    cart_paint_price = '',

    def find_first_painting_and_take_in_cart_it(self):
        with allure.step('Find first painting and take in cart it'):
            wait = WebDriverWait(self.browser, 3)
            paintings = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, locators['post'])))

            like = None
            if (paintings):
                first_painting = paintings[0]
                like = first_painting.find_element(By.CSS_SELECTOR, locators['cart_btn'])
                self.first_paint_name = first_painting.find_element(By.CSS_SELECTOR, locators['paiting_name']).text
                self.cart_paint_price = first_painting.find_element(By.CSS_SELECTOR, locators['paiting_price']).text
                like.click()

            assert like is not None

        return self
    
    def go_to_cart(self):
        with allure.step('Go to cart'):
            go_cart_button = self.browser.find_element(By.CSS_SELECTOR, locators['go_cart_in_modal'])
            if (go_cart_button):
                go_cart_button.click()

        return self
    
    def find_paint_in_cart(self):
        with allure.step('Find paint in cart'):
            wait = WebDriverWait(self.browser, 30)
            paintings = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, locators['cart_item'])))

            found_painting = None
            for painting in paintings:
                temp_name = painting.find_element(By.CSS_SELECTOR, locators['cart_item_name']).text
                temp_price = painting.find_element(By.CSS_SELECTOR, locators['cart_item_price']).text
                if temp_name in self.first_paint_name and temp_price in self.cart_paint_price:
                    found_painting = painting
                    break

            assert found_painting is not None

        return self
