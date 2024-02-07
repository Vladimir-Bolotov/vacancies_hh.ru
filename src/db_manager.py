import psycopg2


def connector(sql, params):
    with psycopg2.connect(dbname='headhunter', **params) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()


class DBManager:

    def __init__(self, params):
        self.params = params

    def get_companies_and_vacancies_count(self):
        """ Получает список всех компаний и количество вакансий у каждой компании."""

        return connector("""SELECT employer_name , COUNT(vacancies.vacancy_id) AS count_vacancies FROM employers
                  JOIN vacancies
                  USING(employer_id)
                  GROUP BY employer_name """,
                         self.params)

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""

        return connector("""SELECT employers.employer_name, vacancy_name, salary, link  FROM  vacancies
                  JOIN employers
                  USING(employer_id)""",
                         self.params)

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""

        return connector("""SELECT AVG(salary) AS avg_salary FROM vacancies""",
                         self.params)

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""

        return connector("""SELECT vacancy_name FROM vacancies 
                  WHERE salary > (SELECT AVG(salary) FROM vacancies)""",
                         self.params)

    def get_vacancies_with_keyword(self, word: str):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""

        return connector(f"""SELECT vacancy_name FROM vacancies 
                  WHERE LOWER(vacancy_name) LIKE '%{word.lower()}%'""",
                         self.params)
