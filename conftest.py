from selenium import webdriver
import pytest
import re


@pytest.fixture
def link(request):
    link = f'http://selenium1py.pythonanywhere.com/{request.config.getoption("--language")}/'
    return link


@pytest.fixture
def browser():
    browser = webdriver.Chrome()
    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture
def languages_initial():
    languages_initial = ['ar', 'ca', 'cs', 'da', 'de', 'en-gb', 'el', 'es', 'fi', 'fr', 'it', 'ko', 'nl', 'pl', 'pt',
                         'pt-br', 'ro', 'ru', 'sk', 'uk', 'zh-hans']
    return languages_initial


@pytest.fixture
def current_language(link, languages_initial):

    if re.findall('\.com/(\w+\-\w+)', link):
        language_list_from_link = re.findall('\.com/(\w+\-\w+)', link)
        if language_list_from_link == ['zh-cn']:
            language_list_from_link = ['zh-hans']
    else:
        language_list_from_link = re.findall('\.com/(\w+)', link)

    assert len(language_list_from_link) == 1, \
        'Ошибка парсинга link при определении значения <language>, ожидается link в формате:\n' \
        'http://selenium1py.pythonanywhere.com/<language>/\nгде <language> - это элемент списка {}.\n' \
        'Проверьте link.'.format(languages_initial)

    if language_list_from_link[0] in languages_initial:
        current_language = language_list_from_link[0]

        return current_language

    else:
        print('{} отсутствует в списке ожидаемых языков. Удостоверьтесь, что значение языка в конце link корректно.'
              ''.format(language_list_from_link[0]))


def pytest_addoption(parser):
    parser.addoption("--language", action="store", default='ru',
                     help="Выбрать язык для загрузки сайта из списка значений:\n")
