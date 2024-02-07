import requests
import psycopg2


def data_api_hh(id_employers: list) -> list[dict]:
    """ Запрашивает данные о вакансиях с HeadHunter.ru"""
    data_vacancies = []
    for id_employer in id_employers:
        url = 'https://api.hh.ru/vacancies'
        params = {'per_page': 20,
                  'employer_id': id_employer,
                  'only_with_salary': True}
        response = requests.get(url, params=params)
        data_vacancies.append(response.json())

    return data_vacancies


def create_db(name_db: str, params: dict) -> None:
    """ Создает базу данных и таблицы в ней"""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE IF EXISTS {name_db}')
    cur.execute(f'CREATE DATABASE {name_db}')

    cur.close()
    conn.close()

    with psycopg2.connect(dbname=name_db, **params) as conn:
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE employers(
                        employer_id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
                        employer_name VARCHAR(100) NOT NULL)""")

            cur.execute("""CREATE TABLE vacancies(
                        vacancy_id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
                        employer_id uuid REFERENCES employers(employer_id),
                        vacancy_name VARCHAR(100),
                        salary INT,
                        link VARCHAR)""")
    conn.commit()


def seve_to_bd(data: list[dict], name_db: str, params: dict) -> None:
    """ Сохраняет данные о вакансиях и компаниях в базу данных"""
    with psycopg2.connect(dbname=name_db, **params) as conn:
        with conn.cursor() as cur:

            for item in data:
                try:
                    name_company = item['items'][0]['employer']['name']

                    cur.execute("""INSERT INTO employers (employer_name) VALUES (%s)
                                RETURNING employer_id""", (name_company,))

                    employer_id = (cur.fetchone()[0])

                    for vacancy in item['items']:
                        vacancy_name = vacancy['name']
                        if vacancy['salary']['from']:
                            salary = vacancy['salary']['from']
                        else:
                            salary = vacancy['salary']['to']
                        link = vacancy['alternate_url']

                        cur.execute("""INSERT INTO vacancies (employer_id, vacancy_name, salary, link)
                                    VALUES (%s, %s, %s, %s)""",
                                    (employer_id, vacancy_name, salary, link))
                except IndexError:
                    print(f'В компании {name_company} (id - {vacancy["employer"]["id"]}) нет открытых вакансий')
                    continue

    conn.commit()
