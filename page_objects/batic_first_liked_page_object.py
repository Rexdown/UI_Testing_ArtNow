import allure

from .base_page_object import ArtnowPageObject
from ..constants.locators import locators

from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
    
class BaticFirstLikedPageObject(ArtnowPageObject):
    def __init__(self, browser: WebDriver):
        super().__init__(browser)
    
    like_paint_name = '',

    def find_first_painting_and_like_it(self):
        with allure.step('Find first painting and like it'):
            wait = WebDriverWait(self.browser, 3)
            paintings = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, locators['post'])))

            like = None
            if (paintings):
                first_painting = paintings[0]
                like = first_painting.find_element(By.CSS_SELECTOR, locators['heart_btn'])
                self.like_paint_name = first_painting.find_element(By.CSS_SELECTOR, locators['paiting_name']).text
                like.click()

            assert like is not None

        return self
    
    def go_to_likes_paints(self):
        with allure.step('Go to likes paints'):
            go_likes_button = self.browser.find_element(By.CSS_SELECTOR, locators['likes_list'])
            if go_likes_button is not None:
                go_likes_button.click()

        return self
    
    def find_liked_paint_in_wishlist(self):
        with allure.step('Find liked paint in wishlist'):
            attempts = 0
            found_painting = None

            # Периодически выпадала ошибка StaleElementReferenceException. Лучше решения, чем это, в интернете не нашел.
            while attempts < 5:
                try:
                    wait = WebDriverWait(self.browser, 30)
                    paintings = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, locators['painting_name_in_list'])))

                    for painting in paintings:
                        if self.like_paint_name in painting.text:
                            found_painting = painting
                            break
                    else:
                        attempts += 1
                except StaleElementReferenceException:
                    continue
                finally:
                    attempts += 1

            assert found_painting is not None
            assert self.like_paint_name in found_painting.text

        return self