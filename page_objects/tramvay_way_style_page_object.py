import allure

from .base_page_object import ArtnowPageObject
from ..constants.locators import locators

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver


class TramvayWayStylePageObject(ArtnowPageObject):
    def __init__(self, browser: WebDriver):
        super().__init__(browser)

    def go_into_tramvay_way_painting(self):
        with allure.step('Go into tramvay way painting'):
            wait = WebDriverWait(self.browser, 3)
            paintings = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, locators['painting'])))

            for painting in paintings:
                if 'Трамвайный путь' in painting.text:
                    painting.click()
                    return self

        return self
    
    def click_on_genre_picker(self, genre):
        genres_picker = self.browser.find_element(By.CSS_SELECTOR, locators['genres_picker'])

        current_genre_label = genres_picker.find_element(By.XPATH, f'//label[contains(text(), "{genre}")]')
        current_genre_label.find_element(By.TAG_NAME, 'input').click()

        with allure.step(f'Click on genre picker on {genre}'):
            assert current_genre_label.find_element(By.TAG_NAME, 'input').is_selected()

            self.browser.find_element(By.CSS_SELECTOR, locators['apply_filter']).click()
            assert current_genre_label.find_element(By.TAG_NAME, 'input').is_selected()

        return self
    
    def check_tramvay_way_painting_genre(self):
        with allure.step('Check tramvay way painting genre'):
            wait = WebDriverWait(self.browser, 3)
            arr = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, locators['genre'])))

            found_genre = None
            for item in arr:
                if 'Городской пейзаж' in item.text:
                    found_genre = item
                    break

            assert found_genre is not None
            assert 'Городской пейзаж' in found_genre.text

        return self