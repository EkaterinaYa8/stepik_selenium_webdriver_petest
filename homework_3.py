from selenium import webdriver
from time import sleep
import re

link = 'http://selenium1py.pythonanywhere.com/ru/'
log_in_registration_link = 'http://selenium1py.pythonanywhere.com/ru/accounts/login/'
# account_link = 'http://selenium1py.pythonanywhere.com/ru/accounts/profile/'

languages_initial = ['ar', 'ca', 'cs', 'da', 'de', 'en-gb', 'el', 'es', 'fi', 'fr', 'it', 'ko', 'nl', 'pl', 'pt',
                     'pt-br', 'ro', 'ru', 'sk', 'uk', 'zh-hans']

if re.findall(".com/(\w+\-\w+)", link):
    language_list_from_link = re.findall(".com/(\w+\-\w+)", link)
    if language_list_from_link == ['zh-cn']:
        language_list_from_link = ['zh-hans']
else:
    language_list_from_link = re.findall(".com/(\w+)", link)

assert len(language_list_from_link) == 1, \
    'Ошибка парсинга link при определении значения <language>, ожидается link в формате:\n' \
    'http://selenium1py.pythonanywhere.com/<language>/\nгде <language> - это элемент списка {}.\n' \
    'Проверьте link.'.format(languages_initial)

if language_list_from_link[0] in languages_initial:
    current_language = language_list_from_link[0]
else:
    print('{} отсутствует в списке ожидаемых языков. Удостоверьтесь, что значение языка в конце link корректно.'
          ''.format(language_list_from_link[0]))


def test_1_1_view_language_nav_bar(link=link, languages_initial=languages_initial, print_test_ok=True):
    """Проверка наличия элементов навигационной панели выбора языка"""


    try:
        browser = webdriver.Chrome()
        browser.get(link)
        browser.implicitly_wait(5)

        # Поиск поля выбора языка с выпадающим списком
        browser.find_element_by_xpath('//form[@id="language_selector"]/div/select[@name="language"]')

        # Список языков, которые можно выбрать на сайте
        languages_nav_bar = [element.get_attribute('value') for element in
                             browser.find_elements_by_xpath(
                                 '//form[@id="language_selector"]/div/select[@name="language"]/option')]

        assert len(languages_initial) == len(languages_nav_bar), 'Количество языков, которое можно выбрать на главной '\
                                                                 'странице сайта={}, не соответствует ожидаемому={}.' \
                                                                 ''.format(len(languages_nav_bar), len(languages_initial))
        for i in range(len(languages_initial)):
            assert languages_initial[i] in languages_nav_bar, '{} отсутствует в списке выбора языков на главной ' \
                                                              'странице сайта.'.format(languages_initial[i])

        # Поиск кнопки применения выбранного языка
        browser.find_element_by_xpath('//form[@id="language_selector"]/button[@type="submit"]')

    finally:
        browser.quit()
    if print_test_ok:
        print('test_1_1_view_language_nav_bar - OK')


def test_1_2_view_log_in_registration_link(link=link, print_test_ok=True):
    """Проверка наличия надписи-ссылки 'Войти или зарегистрироваться'"""


    try:
        browser = webdriver.Chrome()
        browser.get(link)
        browser.implicitly_wait(5)

        # Поиск надписи-ссылки 'Войти или зарегистрироваться'
        browser.find_element_by_xpath('//ul[@class="nav navbar-nav navbar-right"]/li/a[@id="login_link"]')

        # Поиск кликабельной стрелочки слева от надписи-ссылки 'Войти или зарегистрироваться'
        browser.find_element_by_xpath(
            '//ul[@class="nav navbar-nav navbar-right"]/li/a[@id="login_link"]/i[@class="icon-signin"]')

    finally:
        browser.quit()
    if print_test_ok:
        print('test_1_2_view_log_in_registration_link - OK')


def test_1_3_view_home_page_title(link=link, current_language=current_language, print_test_ok=True):
    """Проверка наличия элемента с заголовком Oscar Sandbox.
    Oscar - надпись-ссылка на главную страницу."""


    try:
        browser = webdriver.Chrome()
        browser.get(link)
        browser.implicitly_wait(5)

        # Поиск надписи-ссылки Oscar
        browser.find_element_by_xpath('//div[@class="col-sm-7 h1"]/a')
        if current_language == 'ru':
            assert browser.find_element_by_xpath('//div[@class="col-sm-7 h1"]/a').text == 'Oscar'

        # Поиск заголовка Sandbox справа от Oscar
        browser.find_element_by_xpath('//div[@class="col-sm-7 h1"]/small')
        if current_language == 'ru':
            assert browser.find_element_by_xpath('//div[@class="col-sm-7 h1"]/small').text == 'Sandbox'

    finally:
        browser.quit()
    if print_test_ok:
        print("test_1_3_view_home_page_title - OK")


def test_1_4_view_store_drop_down(link=link, current_language=current_language):
    """Проверка наличия элемента элемента 'Просмотр магазина' и выпадащего списка"""


    try:
        browser = webdriver.Chrome()
        browser.get(link)
        browser.implicitly_wait(5)

        # Поиск элемента "Просмотр магазина"
        browser.find_element_by_xpath(
            '//div[@class="navbar-collapse primary-collapse collapse"]/ul[@class="nav navbar-nav"]')

        # Поиск стрелочки справа от "Просмотр магазина"
        browser.find_element_by_xpath(
            '//li[@class="dropdown active open"]/a[@class="dropdown-toggle"]/b[@class="caret"]')

        # Поиск элементов раскрытого выпадающего списка раздела "Просмотр магазина"
        drop_down_elements = browser.find_elements_by_xpath(
            '//li[@class="dropdown active open"]/ul[@class="dropdown-menu"]/li/a[@href]')

        assert len(drop_down_elements) == 4, 'Количество элементов выпадающего списка раздела "Просмотр магазина"' \
                                             ' не соответствует ожидаемому.'

        shop_drop_down_list = [drop_down_elements[i].text for i in range(len(drop_down_elements))]

        if current_language == 'ru':
            shop_drop_down_list_initial = ['Все товары', 'Clothing', 'Books', 'Предложения']
            for i in range(len(shop_drop_down_list_initial)):
                assert shop_drop_down_list_initial[i] in shop_drop_down_list, '{} отсутствует в списке раздела "Просмотр' \
                                                                              ' магазина".' \
                                                                              ''.format(shop_drop_down_list_initial[i])
    finally:
        browser.quit()
    if link == link:
        print('test_1_4_view_store_drop_down - OK')


def test_1_5_view_basket_button(link=link, print_test_ok=True):
    """Проверка наличия кнопки 'Посмотреть корзину'"""


    try:
        browser = webdriver.Chrome()
        browser.get(link)
        browser.implicitly_wait(5)

        # Поиск кнопки 'Посмотреть корзину' вместе с 'кнопкой-стрелочкой вниз' справа от кнопки 'Посмотреть корзину'
        browser.find_element_by_xpath('//div[@class="basket-mini pull-right hidden-xs"]/span[@class="btn-group"]')

        # Поиск кнопки-стрелочки вниз отдельно справа от кнопки 'Посмотреть корзину'
        browser.find_element_by_xpath('//span[@class="btn-group"]/button[@class="btn btn-default dropdown-toggle"]')

    finally:
        browser.quit()
    if print_test_ok:
        print("test_1_5_view_basket_button - OK")


def test_1_6_view_search_field_button(link=link, print_test_ok=True):
    """Проверка наличия поискового поля и кнопки 'Найти'"""


    try:
        browser = webdriver.Chrome()
        browser.get(link)
        browser.implicitly_wait(5)

        # Поисковое поле
        browser.find_element_by_xpath(
            '//form[@class="navbar-form navbar-right"]/div[@class="form-group"]/input[@type="search"]')

        # Поиск кнопки 'Найти' справа от поискового поля
        browser.find_element_by_xpath('//form[@class="navbar-form navbar-right"]/input[@type="submit"]')

    finally:
        browser.quit()
    if print_test_ok:
        print("test_1_6_view_search_field_button - OK")


def test_1_7_view_log_in_registration_page(link=link, current_language=current_language):
    """Проверка наличия основных элементов страницы 'Войти или зарегистрироваться'"""


    try:
        browser = webdriver.Chrome()
        browser.get(link)
        browser.implicitly_wait(5)

        # Поиск и клик по надписи-ссылке 'Войти или зарегистрироваться'
        log_in_registration_link = browser.find_element_by_xpath(
            '//ul[@class="nav navbar-nav navbar-right"]/li/a[@id="login_link"]')
        log_in_registration_link.click()
        browser.implicitly_wait(5)

        # Путь до текущего раздела
        browser.find_element_by_xpath('//div[@class="page_inner"]/ul[@class="breadcrumb"]')
        if current_language == 'ru':
            assert browser.find_element_by_xpath(
                '//div[@class="page_inner"]/ul[@class="breadcrumb"]/li/a').text == 'Начало'
            assert browser.find_element_by_xpath(
                '//div[@class="page_inner"]/ul[@class="breadcrumb"]/li[@class="active"]').text == 'Войти или зарегистрироваться'


        # Поиск поля для ввода email в форме авторизации
        browser.find_element_by_xpath('//input[@name="login-username"]')

        # Поиск поля для ввода пароля в форме авторизации
        browser.find_element_by_xpath('//input[@name="login-password"]')

        # Поиск кнопки для входа
        browser.find_element_by_xpath('//button[@name="login_submit"]')

        # Поиск поля для ввода email в форме регистрации
        browser.find_element_by_xpath('//input[@name="registration-email"]')

        # Поиск поля для ввода пароля в форме регистрации
        browser.find_element_by_xpath('//input[@name="registration-password1"]')

        # Поиск поля для повторного ввода пароля в форме регистрации
        browser.find_element_by_xpath('//input[@name="registration-password2"]')

        # Поиск кнопки для регистрации
        browser.find_element_by_xpath('//button[@name="registration_submit"]')

    finally:
        browser.quit()

    print('test_1_7_view_log_in_registration_page - OK')


def test_1_8_view_top_log_in_registration_page():
    """Проверка наличия основных элементов шапки страницы 'Войти или зарегистрироваться'"""

    # Проверка наличия элементов навигационной панели выбора языка
    test_1_1_view_language_nav_bar(link=log_in_registration_link, languages_initial=languages_initial,
                                   print_test_ok=False)

    # Проверка наличия надписи-ссылки 'Войти или зарегистрироваться'
    test_1_2_view_log_in_registration_link(link=log_in_registration_link, print_test_ok=False)

    # Проверка наличия элемента с заголовком Oscar Sandbox
    test_1_3_view_home_page_title(link=log_in_registration_link, print_test_ok=False)

    # Проверка наличия кнопки 'Посмотреть корзину'
    test_1_5_view_basket_button(link=log_in_registration_link, print_test_ok=False)

    # Проверка наличия поискового поля и кнопки 'Найти'
    test_1_6_view_search_field_button(link=log_in_registration_link, print_test_ok=False)

    print('test_1_8_view_top_log_in_registration_page - OK')





def registration(link=link, input_email='true_email@test.ru', input_password='truepassw', email=True, password=True,
                 delete_profile=True, cansel_delete_profile=False, current_language=current_language):
    """Регистрация пользователя"""


    try:
        browser = webdriver.Chrome()
        browser.get(link)
        browser.implicitly_wait(5)

        # Переход по ссылке 'Войти или зарегистрироваться'
        log_in_registration_link = browser.find_element_by_xpath(
            '//ul[@class="nav navbar-nav navbar-right"]/li/a[@id="login_link"]')
        log_in_registration_link.click()
        browser.implicitly_wait(5)

        # Ввести email в форме регистрации
        registration_email_field = browser.find_element_by_xpath('//input[@name="registration-email"]')
        registration_email_field.clear()
        sleep(1)
        registration_email_field.send_keys(input_email)

        # Ввести пароль в форме регистрации
        registration_password1_field = browser.find_element_by_xpath('//input[@name="registration-password1"]')
        registration_password1_field.clear()
        sleep(1)
        registration_password1_field.send_keys(input_password)

        # Повторно ввести пароль в форме регистрации
        registration_password2_field = browser.find_element_by_xpath('//input[@name="registration-password2"]')
        registration_password2_field.clear()
        sleep(1)
        registration_password2_field.send_keys(input_password)

        # Нажать кнопку "Зарегистрироваться"
        registration_button = browser.find_element_by_xpath('//button[@name="registration_submit"]')
        browser.implicitly_wait(5)
        registration_button.click()

        # Успешная регистрация, автоматически выполнен вход в аккаунт
        if email and password:
            # Сообщение об успешной регистрации
            success_registration_msg = browser.find_element_by_xpath(
                '//div[@id="messages"]/div[@class="alert alert-success  fade in"]/div[@class="alertinner wicon"]')
            if current_language == 'ru':
                assert success_registration_msg.text == 'Спасибо за регистрацию!', 'Сообщение об успешной регистрации:' \
                                                                                   '\n"{}"\nне совпадает с ожидаемым.' \
                                                                                   ''.format(success_registration_msg.text)

            # Иконка аккаунта
            browser.find_element_by_xpath('//i[@class="icon-user"]')

            # Аккаунт
            account_link = browser.find_element_by_xpath('//ul[@class="nav navbar-nav navbar-right"]/li[1]')
            if current_language == 'ru':
                account_link.text == 'Аккаунт'

            # Кнопка "Выход" из аккаунта
            browser.find_element_by_xpath('//a[@id="logout_link"]/i[@class="icon-signout"]') # стрелочка справа от кнопки
            browser.find_element_by_xpath('//a[@id="logout_link"]')  # кнопка 'Выход'
            if current_language == 'ru':
                assert browser.find_element_by_xpath('//a[@id="logout_link"]').text == 'Выход'

            # Перейти в аккаунт
            enter_account = browser.find_element_by_xpath('//ul[@class="nav navbar-nav navbar-right"]/li[1]')
            sleep(1)
            enter_account.click()
            # Проверка email в таблице аккаунта
            assert browser.find_element_by_xpath(
                '//table[@class="table table-striped table-bordered"]/tbody/tr[2]/td').text == input_email, \
                "Адрес электронной почты в настройках аккаунта не соответствует введённому при регистрации."

            # Кнопки 'Изменить пароль', 'Редактировать профиль', 'Удалить профиль'
            account_buttons = browser.find_elements_by_xpath('//div[@class="col-sm-8 col-md-9"]/a')
            assert len(account_buttons) == 3, \
                "Количество кнопок в настройках аккаунта не соответствует ожидаемому."
            if current_language == 'ru':
                assert account_buttons[0].text == 'Изменить пароль'
                assert account_buttons[1].text == 'Редактировать профиль'
                assert account_buttons[2].text == 'Удалить профиль'

            # Удалить профиль
            """Примечание - Пыталась вместо этого куска кода вставить функцию delete_profile(), в которой в качестве
            аргументов передать browser=browser.current_url (или browser=browser), в теле функции при таком вызове 
            пропускаются browser.get(link) и browser.quit(). После выполнения всех инструкций в текущем окне загружается 
            пустая вкладка и остаётся висеть. Как следует правильно сделать не разобралась :( """

            if delete_profile:
                delete_profile_button = browser.find_elements_by_xpath('//div[@class="col-sm-8 col-md-9"]/a')[2]
                sleep(1)
                delete_profile_button.click()

                # Ввести действующий пароль для подтверждения удаления профиля
                password_field = browser.find_element_by_xpath('//input[@name="password"]')
                password_field.clear()
                sleep(1)
                password_field.send_keys(input_password)

                if cansel_delete_profile:
                    # Нажать кнопку 'Отмена'
                    cansel_delete_button = browser.find_element_by_xpath('//form[@id="delete_profile_form"]/div[3]/a')
                    sleep(1)
                    cansel_delete_button.click()
                    sleep(1)

                    # Удаление отменено автоматически перешли в профиль

                    # Иконка аккаунта
                    browser.find_element_by_xpath('//i[@class="icon-user"]')

                    # Аккаунт
                    browser.find_element_by_xpath('//ul[@class="nav navbar-nav navbar-right"]/li[1]')

                    # Кнопка "Выход" из аккаунта
                    browser.find_element_by_xpath(
                        '//a[@id="logout_link"]/i[@class="icon-signout"]')  # стрелочка справа от кнопки
                    browser.find_element_by_xpath('//a[@id="logout_link"]')  # кнопка 'Выход'

                    # Адрес электронной почты в настройках аккаунта
                    browser.find_element_by_xpath('//table[@class="table table-striped table-bordered"]/tbody/tr[2]/td')

                    # Кнопки 'Изменить пароль', 'Редактировать профиль', 'Удалить профиль'
                    browser.find_elements_by_xpath('//div[@class="col-sm-8 col-md-9"]/a')
                    sleep(1)

                    # Удалить профиль для очистки среды тестирования
                    delete_profile_button = browser.find_elements_by_xpath('//div[@class="col-sm-8 col-md-9"]/a')[2]
                    sleep(1)
                    delete_profile_button.click()

                    # Ввести действующий пароль для подтверждения удаления профиля
                    password_field = browser.find_element_by_xpath('//input[@name="password"]')
                    password_field.clear()
                    sleep(1)
                    password_field.send_keys(input_password)

                    # Нажать кнопку 'Удалить'
                    delete_button = browser.find_element_by_xpath('//button[@class="btn btn-lg btn-danger"]')
                    sleep(1)
                    delete_button.click()

                    success_deleted_msg = browser.find_element_by_xpath('//div[@class="alertinner wicon"]')
                    if current_language == 'ru':
                        assert success_deleted_msg.text == 'Ваш профиль удален. Спасибо, что воспользовались нашим сайтом.', \
                            'Сообщение об успешном удалении профиля:\n"{}"\nНе совпадает с ожидаемым.' \
                            ''.format(success_deleted_msg.text)

                else:
                    # Нажать кнопку 'Удалить'
                    delete_button = browser.find_element_by_xpath('//button[@class="btn btn-lg btn-danger"]')
                    sleep(1)
                    delete_button.click()

                    success_deleted_msg = browser.find_element_by_xpath('//div[@class="alertinner wicon"]')
                    if current_language == 'ru':
                        assert success_deleted_msg.text == 'Ваш профиль удален. Спасибо, что воспользовались нашим сайтом.', \
                            'Сообщение об успешном удалении профиля:\n"{}"\nНе совпадает с ожидаемым.' \
                            ''.format(success_deleted_msg.text)

        else:
            # Поиск надписи-ссылки 'Войти или зарегистрироваться'
            browser.find_element_by_xpath('//ul[@class="nav navbar-nav navbar-right"]/li/a[@id="login_link"]')

            # Поиск кликабельной стрелочки слева от надписи-ссылки 'Войти или зарегистрироваться'
            browser.find_element_by_xpath(
                '//ul[@class="nav navbar-nav navbar-right"]/li/a[@id="login_link"]/i[@class="icon-signin"]')

            if email and input_password != '':  # password=False
                # Ошибка регистрации
                registration_error_msg = browser.find_element_by_xpath('//div[@class="alert alert-danger"]')
                if current_language == 'ru':
                    assert registration_error_msg.text == 'Опаньки! Мы нашли какие-то ошибки - пожалуйста, ' \
                                                          'проверьте сообщения об ошибках ниже и попробуйте еще раз',\
                        'Сообщение об ошибке регистрации:\n{}\nНе совпадает с ожидаемым.' \
                        ''.format(registration_error_msg.text)
            # else:
            #     # Не получилось поймать alert, почему-то не находится :(
            #     sleep(3)
            #     alert = browser.switch_to.alert
            #     print(alert.text)

    finally:
        browser.quit()



def log_in(link=link, input_email='true_email@test.ru', input_password='truepassw', input_new_password='truepassw1',
           log_in=True, pre_registration=True, repeate_log_in=False, change_password=False, new_password=True,
           delete_profile=True, current_language=current_language):
    """Аутентификация пользователя"""


    if pre_registration:
        registration(link=link, delete_profile=False)

    try:
        browser = webdriver.Chrome()
        browser.get(link)
        browser.implicitly_wait(5)


        def delete_pass():
            delete_profile_button = browser.find_elements_by_xpath('//div[@class="col-sm-8 col-md-9"]/a')[2]
            sleep(2)
            delete_profile_button.click()

            # Ввести действующий пароль для подтверждения удаления профиля
            password_field = browser.find_element_by_xpath('//input[@name="password"]')
            password_field.clear()
            sleep(1)

            if (not change_password) or (change_password and (not new_password)):
                password_field.send_keys('truepassw')
            else:
                password_field.send_keys('truepassw1')

            # Нажать кнопку 'Удалить'
            delete_button = browser.find_element_by_xpath('//button[@class="btn btn-lg btn-danger"]')
            sleep(2)
            delete_button.click()

            success_deleted_msg = browser.find_element_by_xpath('//div[@class="alertinner wicon"]')
            if current_language == 'ru':
                assert success_deleted_msg.text == 'Ваш профиль удален. Спасибо, что воспользовались нашим сайтом.', \
                    'Сообщение об успешном удалении профиля:\n"{}"\nНе совпадает с ожидаемым.' \
                    ''.format(success_deleted_msg.text)

        def delete_profile():
            """Удаление профиля"""

            if delete_profile:
                if log_in:
                    delete_pass()
                else:
                    # Перейти в аккаунт
                    enter_account = browser.find_element_by_xpath('//ul[@class="nav navbar-nav navbar-right"]/li[1]')
                    sleep(1)
                    enter_account.click()
                    delete_pass()

        def log_in_pass(input_email=input_email, input_password=input_password, skip_check=False):
            # Переход по ссылке 'Войти или зарегистрироваться'
            log_in_registration_link = browser.find_element_by_xpath(
                '//ul[@class="nav navbar-nav navbar-right"]/li/a[@id="login_link"]')
            log_in_registration_link.click()
            browser.implicitly_wait(5)

            # Ввести email в форме авторизации
            log_in_email_field = browser.find_element_by_xpath('//input[@name="login-username"]')
            log_in_email_field.clear()
            sleep(1)
            log_in_email_field.send_keys(input_email)

            # Ввести пароль в форме авторизации
            log_in_password_field = browser.find_element_by_xpath('//input[@name="login-password"]')
            log_in_password_field.clear()
            sleep(1)
            log_in_password_field.send_keys(input_password)

            # Нажать кнопку Войти"
            log_in_button = browser.find_element_by_xpath('//button[@name="login_submit"]')
            browser.implicitly_wait(5)
            log_in_button.click()

            if not skip_check:
                if log_in:
                    # Сообщение об успешной аутентификации
                    success_log_in_msg = browser.find_element_by_xpath(
                        '//div[@id="messages"]/div[@class="alert alert-success  fade in"]/div[@class="alertinner wicon"]')
                    if current_language == 'ru':
                        assert success_log_in_msg.text == 'Рады видеть вас снова', 'Сообщение об успешной аутентификации:' \
                                                                                   '\n""{}"\nне совпадает с ожидаемым.' \
                                                                                   ''.format(success_log_in_msg.text)
                    # Иконка аккаунта
                    browser.find_element_by_xpath('//i[@class="icon-user"]')

                    # Аккаунт
                    account_link = browser.find_element_by_xpath('//ul[@class="nav navbar-nav navbar-right"]/li[1]')
                    if current_language == 'ru':
                        account_link.text == 'Аккаунт'

                    # Кнопка "Выход" из аккаунта
                    browser.find_element_by_xpath('//a[@id="logout_link"]/i[@class="icon-signout"]') # стрелочка справа от кнопки
                    browser.find_element_by_xpath('//a[@id="logout_link"]')  # кнопка 'Выход'
                    if current_language == 'ru':
                        assert browser.find_element_by_xpath('//a[@id="logout_link"]').text == 'Выход'

                    # Перейти в аккаунт
                    enter_account = browser.find_element_by_xpath('//ul[@class="nav navbar-nav navbar-right"]/li[1]')
                    sleep(2)
                    enter_account.click()
                    # Проверка email в таблице аккаунта
                    assert browser.find_element_by_xpath(
                        '//table[@class="table table-striped table-bordered"]/tbody/tr[2]/td').text == input_email, \
                        "Адрес электронной почты в настройках аккаунта не соответствует введённому при регистрации."

                    # Кнопки 'Изменить пароль', 'Редактировать профиль', 'Удалить профиль'
                    account_buttons = browser.find_elements_by_xpath('//div[@class="col-sm-8 col-md-9"]/a')
                    assert len(account_buttons) == 3, \
                        "Количество кнопок в настройках аккаунта не соответствует ожидаемому."
                    if current_language == 'ru':
                        assert account_buttons[0].text == 'Изменить пароль'
                        assert account_buttons[1].text == 'Редактировать профиль'
                        assert account_buttons[2].text == 'Удалить профиль'

                else:
                    # Ошибка аутентификации
                    log_in_error_msg = browser.find_element_by_xpath('//div[@class="alert alert-danger"]')
                    if current_language == 'ru':
                        assert log_in_error_msg.text == 'Опаньки! Мы нашли какие-то ошибки - пожалуйста, ' \
                                                        'проверьте сообщения об ошибках ниже и попробуйте еще раз', \
                            'Сообщение об ошибке аутентификации:\n{}\nНе совпадает с ожидаемым.' \
                            ''.format(log_in_error_msg.text)


        if log_in:
            if repeate_log_in:
                # Выйти из профиля
                exit_account = browser.find_element_by_xpath('//a[@id="logout_link"]')
                sleep(2)
                exit_account.click()
                sleep(2)
                log_in_pass()
            if change_password:
                log_in_pass()

                # Нажать кнопку 'Изменить пароль'
                change_password_button = browser.find_elements_by_xpath('//div[@class="col-sm-8 col-md-9"]/a')[0]
                sleep(2)
                change_password_button.click()

                # Ввести старый пароль
                old_password_field = browser.find_element_by_xpath('//input[@name="old_password"]')
                old_password_field.clear()
                sleep(1)
                old_password_field.send_keys(input_password)

                # Ввести новый пароль
                new_password1_field = browser.find_element_by_xpath('//input[@name="new_password1"]')
                new_password1_field.clear()
                sleep(1)
                new_password1_field.send_keys(input_new_password)

                if new_password:
                    # Повторно ввести новый пароль
                    new_password2_field = browser.find_element_by_xpath('//input[@name="new_password2"]')
                    new_password2_field.clear()
                    sleep(1)
                    new_password2_field.send_keys(input_new_password)
                else:
                    # Ввести пароль, отличный от нового пароля в первом поле
                    new_password2_field = browser.find_element_by_xpath('//input[@name="new_password2"]')
                    new_password2_field.clear()
                    sleep(1)
                    new_password2_field.send_keys('falsepass1')

                # Нажать кнопку "Сохранить"
                save_button = browser.find_element_by_xpath(
                    '//form[@id="change_password_form"]/div[4]/div/button[@type="submit"]')
                browser.implicitly_wait(5)
                save_button.click()

                if new_password:
                    success_msg = browser.find_element_by_xpath(
                        '//div[@id="messages"]/div[@class="alert alert-success  fade in"]/div[@class="alertinner wicon"]')
                    if current_language == 'ru':
                        assert success_msg.text == 'Пароль обновлён'

                    # Выйти из профиля
                    exit_account = browser.find_element_by_xpath('//a[@id="logout_link"]')
                    sleep(1)
                    exit_account.click()
                    sleep(1)
                    log_in_pass(input_password=input_new_password)
                else:
                    # Ошибка изменения пароля
                    change_password_error_msg = browser.find_element_by_xpath('//div[@class="alert alert-danger"]')
                    if current_language == 'ru':
                        assert change_password_error_msg.text == 'Опаньки! Мы нашли какие-то ошибки - пожалуйста, ' \
                                                        'проверьте сообщения об ошибках ниже и попробуйте еще раз', \
                            'Сообщение об ошибке аутентификации:\n{}\nНе совпадает с ожидаемым.' \
                            ''.format(change_password_error_msg.text)

                    # Перейти в аккаунт
                    enter_account = browser.find_element_by_xpath('//ul[@class="nav navbar-nav navbar-right"]/li[1]')
                    sleep(1)
                    enter_account.click()

            delete_profile()

        else:
            log_in_pass()
            log_in_pass(input_email='true_email@test.ru', input_password='truepassw', skip_check=True)
            delete_profile()

    finally:
        browser.quit()









def test_2_1_registration_true_data_and_delete_profile():
    """Регистрация. email - корректный, пароль - 9 символов. Затем удаление созданного профиля."""

    # input_email='true_email@test.ru', input_password='truepassw'
    registration(link=link)
    print('test_2_1_registration_true_data_and_delete_profile - OK')


def test_2_2_registration_false_password():
    """Регистрация. email - корректный, некорректный пароль - 8 символов (короткий пароль)"""

    # input_email='true_email@test.ru'
    registration(link=link, input_password='12345678', password=False)
    print('test_2_2_registration_false_password - OK')


def test_2_3_registration_false_email():
    """Регистрация. email - не содержит знак '@', корректный пароль - 9 символов"""

    # input_password='truepassw'
    registration(link=link, input_email='email_test.ru', email=False)
    print('test_2_3_registration_false_email - OK')


def test_2_4_registration_empty_password():
    """Регистрация. email - корректный, пустое поле пароля"""

    # input_email='true_email@test.ru'
    registration(link=link, input_password='', password=False)
    print('test_2_4_registration_empty_password - OK')


def test_2_5_registration_empty_email():
    """Регистрация. Пустое поле email, корректный пароль - 9 символов"""

    # input_password='truepassw'
    registration(link=link, input_email='', email=False)
    print('test_2_5_registration_empty_email - OK')


def test_2_6_registration_empty_email_and_password():
    """Регистрация. Пустое поле email, пустое поле пароля"""

    # input_email='true_email@test.ru'
    registration(link=link, input_email='', email=False, input_password='', password=False)
    print('test_2_6_registration_empty_email_and_password - OK')


def test_2_7_log_in_true_data():
    """Аутентификация пользователя. Зарегистрированный email, корректный пароль."""

    # input_email='true_email@test.ru', input_password='truepassw'
    log_in(link=link)
    print('test_2_3_log_in_true_data - OK')


def test_2_8_repeate_log_in():
    """Аутентификация пользователя. Выход из профиля. Повторная аутентификация"""

    # input_email='true_email@test.ru', input_password='truepassw'
    log_in(link=link, repeate_log_in=True)
    print('test_2_4_repeate_log_in - OK')


def test_2_7_log_in_false_email():
    """Аутентификация пользователя. Незарегистрированный email, корректный пароль."""

    # input_email=False, input_password='truepassw'
    log_in(link=link, input_email='false_email@test.ru', log_in=False)
    print('test_2_7_log_in_false_email - OK')


def test_2_8_log_in_false_password():
    """Аутентификация пользователя. Зарегистрированный email, некорректный пароль."""

    # input_email='true_email@test.ru', input_password=False
    log_in(link=link, input_password='falsepassw', log_in=False)
    print('test_2_8_log_in_false_password - OK')


def test_2_9_change_password_true_data():
    """Изменение пароля. Новый пароль - корректный, отличается от старого"""

    log_in(link=link, change_password=True)
    print('test_2_9_change_password_true_data - OK')


def test_2_10_change_password_false_data():
    """Изменение пароля. При измении пароля повторно вводится пароль,
    отличный от пароля, введённого в первом поле"""

    log_in(link=link, change_password=True, new_password=False)
    print('test_2_10_change_password_false_data - OK')


def test_2_11_cansel_delete_profile():
    """Отмена удаления профиля пользователя"""

    registration(link=link, delete_profile=True, cansel_delete_profile=True)
    print('test_2_11_cansel_delete_profile')








def test_1_9_view_basket_button(link=link):
    """Проверка наличия элемента с заголовком Oscar Sandbox"""


    try:
        browser = webdriver.Chrome()
        browser.get(link)
        browser.implicitly_wait(5)

        # Поиск кнопки 'Посмотреть корзину' вместе с 'кнопкой-стрелочкой вниз' справа от кнопки 'Посмотреть корзину'
        browser.find_element_by_xpath('//div[@class="basket-mini pull-right hidden-xs"]/span[@class="btn-group"]')

        # Поиск кнопки-стрелочки вниз отдельно справа от кнопки 'Посмотреть корзину'
        browser.find_element_by_xpath('//span[@class="btn-group"]/button[@class="btn btn-default dropdown-toggle"]')

        # Поиск элемента 'Просмотр магазина'
        browser.find_element_by_xpath('//div[@class="navbar-collapse primary-collapse collapse"]/ul[@class="nav navbar-nav"]')

        # Поиск элементов раскрытого выпадающего списка под элементом 'Просмотр магазина'
        browser.find_element_by_xpath('//li[@class="dropdown active open"]/ul[@class="dropdown-menu"]')

        print("test_1_5_view_basket_button - OK")


    finally:
        sleep(1)
        browser.quit()



print("\n=========================== test session starts ===========================\n")
# test_1_1_view_language_nav_bar()
# test_1_2_view_log_in_registration_link()
# test_1_3_view_home_page_title()
# test_1_4_view_store_drop_down()
# test_1_5_view_basket_button()
# test_1_6_view_search_field_button()
# test_1_7_view_log_in_registration_page()
# test_1_8_view_top_log_in_registration_page()
# test_2_1_registration_true_data_and_delete_profile()
# test_2_2_registration_false_password()
# test_2_3_registration_false_email()
# test_2_4_registration_empty_password()
# test_2_5_registration_empty_email()
# test_2_6_registration_empty_email_and_password()
# test_2_7_log_in_false_email()
# test_2_8_log_in_false_password()
# test_2_9_change_password_true_data()
# test_2_10_change_password_false_data()
# test_2_11_cansel_delete_profile()






# не забываем оставить пустую строку в конце файла
