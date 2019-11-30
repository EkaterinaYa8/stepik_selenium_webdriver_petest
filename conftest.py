from selenium import webdriver
import pytest


@pytest.fixture
def languages_initial():
    languages_initial = ['ar', 'ca', 'cs', 'da', 'de', 'en-gb', 'el', 'es', 'fi', 'fr', 'it', 'ko', 'nl', 'pl', 'pt',
                         'pt-br', 'ro', 'ru', 'sk', 'uk', 'zh-hans']
    return languages_initial


@pytest.fixture
def link(request, languages_initial):
    link = f'http://selenium1py.pythonanywhere.com/{request.config.getoption("--language")}/'

    language_from_link = request.config.getoption("--language")
    if language_from_link == 'zh-cn':
        return link
    elif language_from_link == 'zh-hans':
        return 'http://selenium1py.pythonanywhere.com/zh-cn/'
    else:
        assert language_from_link in languages_initial, f'Переданное значение языка в аргументах командной строки ' \
                                                        f'--language={request.config.getoption("--language")} ' \
                                                        f'некорректно.\nДолжно быть использовано значение из следующего ' \
                                                        f'списка:\n{languages_initial} или \"zh-cn\".'
        return link


@pytest.fixture
def browser():
    browser = webdriver.Chrome()
    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture
def current_language(request):
    current_language = request.config.getoption("--language")
    return current_language


def pytest_addoption(parser):
    parser.addoption('--language', action='store', default='ru',
                     help='Выбрать язык для загрузки сайта из списка значений:\n')
