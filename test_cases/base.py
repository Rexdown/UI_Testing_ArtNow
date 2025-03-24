from selenium import webdriver


def get_webdriver(type='Chrome'):
    match type:
        case 'Firefox':
            return webdriver.Firefox()
        case 'Chrome':
            return webdriver.Chrome()
