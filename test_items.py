from selenium import webdriver
import pytest


def test_check_add_to_basket_button_on_product_page(browser, link):
    """Страница товара загружается по клику на наименование товара.
    Проверяется наличие кнопки добавления в корзину на странице товара."""

    browser.get(link)
    browser.implicitly_wait(10)

    # Перейти в раздел 'Все товары'
    all_products_link = browser.find_elements_by_xpath(
        '//li[@class="dropdown active open"]/ul[@class="dropdown-menu"]/li/a[@href]')[0]
    browser.implicitly_wait(5)
    all_products_link.click()
    browser.implicitly_wait(10)

    all_products_on_current_page = browser.find_elements_by_xpath(
        '//li[@class="col-xs-6 col-sm-4 col-md-3 col-lg-3"]')

    for i in range(1, len(all_products_on_current_page) + 1):

        # Если товар в наличии
        if len(browser.find_elements_by_xpath(
                '//li[{}]/article/div[@class="product_price"]/p[@class="instock availability"]'
                ''.format(i))) != 0:

            # Перейти на страницу товара по клику на название
            product_name_link = browser.find_element_by_xpath(
                '//li[{}]/article/h3/a'.format(i))
            browser.implicitly_wait(10)
            product_name_link.click()

            product_name = browser.find_element_by_xpath('//div[@class="col-sm-6 product_main"]/h1').text

            assert len(browser.find_elements_by_xpath(
                '//form[@id="add_to_basket_form"]/button[@type="submit"]')) != 0, \
                'На странице товара с наименованием: "{}" со статусом "в наличии" отсутствует кнопка ' \
                '"Добавить в корзину".'.format(product_name)
            break

        elif i == len(all_products_on_current_page) + 1:
            print('На странице нет ни одного товара в наличии.')
        else:
            continue
