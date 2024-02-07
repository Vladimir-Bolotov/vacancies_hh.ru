from src.utils import data_api_hh, create_db, seve_to_bd
from config import config
from src.db_manager import DBManager


def main():
    list_id_company = [8550, 3473336, 41862, 2770726, 974305, 3903645, 688499, 9498112, 3177, 1740]
    data = data_api_hh(list_id_company)
    create_db('headhunter', params)
    seve_to_bd(data, 'headhunter', params)


if 'main' in __name__:
    params = config(filename='../database.ini')
    db = DBManager(params)

    help_ = """    help - выводит список команд
    update - обновить базу данных
    company -  вывести список всех компаний и количество вакансий у каждой компании.
    all - вывести список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
    avg - вывести среднюю зарплату по вакансиям.
    higher salary - вывести список всех вакансий, у которых зарплата выше средней по всем вакансиям
    search - вывести список всех вакансий, в названии которых содержится переданное слово
    exit - выход"""

    print('Здравствуйте!')
    while True:
        user_input = input('Введите команду\n')
        if user_input.lower() == 'help':
            print(help_)

        elif user_input.lower() == 'update':
            main()
            print("База обновлена.")

        elif user_input.lower() == 'company':
            company = db.get_companies_and_vacancies_count()
            for item in company:
                print(f"Компания - {item[0]}, всего вакансий - {item[1]}")

        elif user_input.lower() == 'all':
            all_ = db.get_all_vacancies()
            for vacancy in all_:
                print(vacancy)

        elif user_input.lower() == 'avg':
            avg_salary = int(db.get_avg_salary()[0][0])
            print(f'Средняя зарплата - {avg_salary} руб.')

        elif user_input.lower() == 'higher salary':
            vacancies = db.get_vacancies_with_higher_salary()
            for vacancy in vacancies:
                print(vacancy[0])
        elif user_input.lower() == 'search':
            user_word = input('Введите слово для поиска\n')
            vacancies = db.get_vacancies_with_keyword(user_word)
            for vacancy in vacancies:
                print(vacancy[0])

        elif user_input.lower() == 'exit':
            print("До встречи!")
            break
        else:
            print("Нет такой команды!")
