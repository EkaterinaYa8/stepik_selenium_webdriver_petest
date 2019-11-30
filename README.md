
Ссылка на курс "Автоматизация UI-тестирования на Python" - https://stepik.org/course/58297/syllabus

`test_items.py` - содержит решение Домашнего задания № 4, Часть 1.

`test_gen_selenium_ide` - содержит код, сгенерированный экспортом шагов из Selenium IDE. Решение Домашнего задания № 4, Часть 2.

`diff_between_generate_tests_and_manual_tests.txt` - содержит тезисно отличительные особенности кода, экспортированного из рекордера, 
по сравнению с кодом, написанным вручную. Решение Домашнего задания № 4, Часть 2.

`test_all_web_site_tests.py` - содержит реализацию тестов с помощью PyTest+Selenium Webdriver 
для сайта http://selenium1py.pythonanywhere.com/<language>, где language передаётся в параметрах командной строки, по умолчанию --language=ru.


======================================Linux_OS======================================
1. Создать виртуальное окружение:

	```bash
	sudo apt-get install python3-venv
	mkdir ~/env
	cd ~/env
	python3 -m venv py3
	```

2. Активировать виртуальное окружение:

	```bash
	cd ~/env
	source py3/bin/activate		# чтобы деактивировать виртуальное окружение - deactivate
	```

3. Установить необходимые библиотеки:

	```bash
	pip install -r requirements.txt

	```
4. Запуск автотестов из консоли:

	```bash
	pytest -v -s test_all_web_site_tests.py
	```
   - Для запуска отдельных тестов добавляется ключ `-k`

	```bash
	-k <test_name>
	```
	Например:
		```bash
	-k <test_1_1_view_language_nav_bar>
	```
