from src.utils import data_api_hh, create_db, seve_to_bd
from config import config


def main():
    params = config()
    list_id_company = [5401589, 3473336, 41862, 2770726, 974305, 3903645, 688499, 9498112, 3177, 1740]

    data = data_api_hh(list_id_company)
    create_db('HeadHunter', params)
    seve_to_bd(data, 'HeadHunter', params)


if 'main' in __name__:
    main()
