import pytest
import allure

from selenium.common.exceptions import StaleElementReferenceException

from .base import get_webdriver

from ..page_objects.vishitie_page_object import VishitiePageObject
from ..page_objects.tramvay_way_style_page_object import TramvayWayStylePageObject
from ..page_objects.batic_first_liked_page_object import BaticFirstLikedPageObject
from ..page_objects.search_giraf_page_object import SearchGirafPageObject
from ..page_objects.put_jewelry_painting_to_cart_page_object import PutJewelryPaintingToCartPageObject


def make_test(func):
    func.__test__ = True

    return func


@pytest.fixture(scope="session")
def browser():
    driver = get_webdriver()
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs['browser']
        allure.attach(driver.get_screenshot_as_png(), name="screenshot", attachment_type=allure.attachment_type.PNG)


@allure.title('Трамвайный путь №1')
@allure.epic('epic')
@allure.feature('feature')
@allure.story('story')
@allure.testcase('Проверка наличия картины "Трамвайный путь" в "Вышитые картины" с жанром "Городской пейзаж"')
@make_test
def test_1(browser):
    artnow_page = VishitiePageObject(browser)
    try:
        artnow_page \
            .go_to_menu_item_page(link_text='Вышитые картины',
                                title_text='вышитые картины',
                                steps=[
                                    'Find extra menu items expand button',
                                    'Click extra menu items expand button',
                                    'Go to vishitie kartiny page'
                                ]) \
            .click_on_genre_picker('Городской пейзаж') \
            .find_tramvay_way_painting()
    except (AssertionError, StaleElementReferenceException):
        allure.attach(browser.get_screenshot_as_png(), name="screenshot", attachment_type=allure.attachment_type.PNG)
        raise
    

@allure.title('Трамвайный путь №2')
@allure.testcase('Проверка, что стиль картины "Трамвайный путь" соответствует жанру "Реализм"')
@make_test
def test_2(browser):
    artnow_page = TramvayWayStylePageObject(browser)
    try:
        artnow_page \
            .go_to_menu_item_page(link_text='Вышитые картины',
                                title_text='вышитые картины',
                                steps=[
                                    'Find extra menu items expand button',
                                    'Click extra menu items expand button',
                                    'Go to vishitie kartiny page'
                                ]) \
            .click_on_genre_picker('Городской пейзаж') \
            .go_into_tramvay_way_painting() \
            .check_tramvay_way_painting_genre()
    except (AssertionError, StaleElementReferenceException):
        allure.attach(browser.get_screenshot_as_png(), name="screenshot", attachment_type=allure.attachment_type.PNG)
        raise

@allure.title('Добавление в избранное')
@allure.testcase('ПРоверка, что при добавлении картины в избранное из "Батик", она появляется в соответсвующем разделе')
@make_test
def test_3(browser):
    artnow_page = BaticFirstLikedPageObject(browser)
    try:
        artnow_page \
            .go_to_menu_item_page(link_text='Батик',
                                title_text='батик',
                                steps=[
                                    'Go to batic paintings page',
                                    'Click extra menu items expand button',
                                    'Go to batic page'
                                ]) \
            .find_first_painting_and_like_it() \
            .go_to_likes_paints() \
            .find_liked_paint_in_wishlist()
    except (AssertionError, StaleElementReferenceException):
        allure.attach(browser.get_screenshot_as_png(), name="screenshot", attachment_type=allure.attachment_type.PNG)
        raise
    

@allure.title('Работа поисковика')
@allure.testcase('Проверка, что при поиске картин по тесту "Жираф", у первой картины в названии будет содердаться это слово')
@make_test
def test_4(browser):
    artnow_page = SearchGirafPageObject(browser)
    try:
        artnow_page \
            .print_giraf_in_sarch_and_enter() \
            .check_first_paint_after_search()
    except (AssertionError, StaleElementReferenceException):
        allure.attach(browser.get_screenshot_as_png(), name="screenshot", attachment_type=allure.attachment_type.PNG)
        raise


@allure.title('Работа корзины')
@allure.testcase('Проверка, что при добавлении картины из "Ювелирное искусство" в корзину, она появляется в соответсвующем разделе без изменения цены')
@make_test
def test_5(browser):
    artnow_page = PutJewelryPaintingToCartPageObject(browser)
    try:
        artnow_page \
        .go_to_menu_item_page(link_text='Ювелирное искусство',
                              title_text='ювелирные украшения',
                              steps=[
                                  'Go to jewelry paintings page',
                                  'Click extra menu items expand button',
                                  'Go to jewelry paintings page'
                              ]) \
        .find_first_painting_and_take_in_cart_it() \
        .go_to_cart() \
        .find_paint_in_cart()
    except (AssertionError, StaleElementReferenceException):
        allure.attach(browser.get_screenshot_as_png(), name="screenshot", attachment_type=allure.attachment_type.PNG)
        raise
        
    browser.quit()
