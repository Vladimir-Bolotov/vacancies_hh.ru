# vacancies_hh.ru
Программа берет вакансии с сайта HeadHunter.ru, записывает в базу данных и выводит в консоль.

Установка:

    Создать в корневой папке файл database.ini с параметрами подключения к базе данных

Список команд:
    
    help - выводит с писок команд
    update - обновить базу данных
    company -  вывести список всех компаний и количество вакансий у каждой компании.
    all - вывести список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
    avg - вывести среднюю зарплату по вакансиям.
    above avg - вывести список всех вакансий, у которых зарплата выше средней по всем вакансиям
    search - вывести список всех вакансий, в названии которых содержится переданное слово
    exit - выход

Как пользоваться:

    Запустить файл src/main.py и вводить интересующие команды