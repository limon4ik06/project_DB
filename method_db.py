import json
from wsgiref import validate
import psycopg2
import uuid
from psycopg2 import OperationalError, Error
from datetime import datetime, timezone
import re

def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def conection_close(conection, cursor):
    cursor.close()
    conection.close()


def print_table(cursor, statistics=True):
    try:
        if statistics:
            cursor.execute('select categories from cn_requests_hist')
            output_data = cursor.fetchall()
            data = []
            for el in output_data:
                for i in el:
                    for j in i:
                        data.append(j)
            return data, len(output_data)
        else:
            cursor.execute('select * from cn_requests_hist')
            output_data = cursor.fetchall()
            for el in output_data:
                print(el)
    except(Exception, Error) as error:
        print('Ошибка вывода таблицы', error)


def add_part(conection, cursor, categories, phone_number, timeout):
    try:
        cursor.execute('Select max(id) from cn_requests_hist')
        last_id = cursor.fetchall()
        new_id = last_id[-1][0] + 1
        id_request = uuid.uuid4()
        id_status = 4
        requestor_id_peers = 'test'
        categories = json.dumps(categories)
        flag = False
        checker = re.compile(r'(^[+0-9]{1,3})*([0-9]{10,11}$)')
        while not flag:
            if checker.search(phone_number):
                flag = True
            else:
                raise Error('You entered not valid phone number')
        key_value = {"key": "phone", "value": phone_number}
        key_value = json.dumps(key_value)
        time_now = datetime.now(timezone.utc).astimezone().isoformat()
        data = (new_id, id_request, id_status, categories, key_value, requestor_id_peers, time_now, timeout, time_now)
        cursor.execute(f"INSERT INTO cn_requests_hist VALUES{data}")
        conection.commit()
    except(Exception, Error) as error:
        print('Ошибка добавления строки в таблицу', error)


def delete_part(conection, cursor):
    try:
        id_for_delete = f"'{input('id_for_delete: ')}'"
        cursor.execute(f'DELETE FROM cn_requests_hist WHERE id_request = {id_for_delete}')
        conection.commit()
    except(Exception, Error) as error:
        print('Ошибка при удалении', error)
    finally:
        print('Удалено')


def get_statistics(cursor, category):
    data = print_table(cursor)
    result = data[0].count(category)
    return f'requests for {category}: {result}'


def get_all_statistics(cursor):
    data = print_table(cursor)
    categories = []
    for i in data[0]:
        if i not in categories:
            categories.append(i)

    for i in range(len(categories)):
        print(categories[i], data[0].count(categories[i]))
    print('total requests:', data[1])


conection = create_connection('project', 'postgres', 'Ily12Dima06', '127.0.0.1', '5432')
cursor = conection.cursor()
