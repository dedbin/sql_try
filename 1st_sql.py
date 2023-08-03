import sqlite3 as sq


def create_table(name):
    """
    Создать таблицу
    :param name: имя
    """
    with sq.connect('test.db') as con:
        cur = con.cursor()
        cur.execute(f'''
        CREATE TABLE IF NOT EXISTS '{name}'(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            sex INTEGER,
            age INTEGER,
            score INTEGER DEFAULT 0
        )
        ''')


def drop_table(name):
    """
    Удалить таблицу
    :param name: имя
    """
    with sq.connect('test.db') as con:
        cur = con.cursor()
        cur.execute(f'''DROP TABLE IF EXISTS '{name}'
                ''')


def insert_data(data: dict):
    """
    вставить данные
    :param data: передавать словарь в формате {'name': 'test', 'sex': 1, 'age': 1, 'score': 1}
    """
    with sq.connect('test.db') as con:
        cur = con.cursor()
        cur.execute(f'''
        INSERT INTO users(name, sex, age, score)
        VALUES('{data['name']}', {data['sex']}, {data['age']}, {data['score']})
        ''')
    print(cur.fetchall())


def update_data(t_name, user_id, what, value, ):
    """
    Обновить данные
    :param t_name: имя таблицы
    :param what: что обновлять
    :param value: на что
    :param user_id: у кого
    """
    with sq.connect('test.db') as con:
        cur = con.cursor()
        cur.execute(f'''
        UPDATE {t_name} SET {what} = {value} WHERE user_id LIKE {user_id}
        ''')
    print(cur.fetchall())


def delete_user(t_name, user_id=None, name=None):
    """
    Удалить данные пользователя
    :param t_name: имя таблицы
    :param user_id: у кого в формате int
    :param name: у кого в формате str
    """
    with sq.connect('test.db') as con:
        cur = con.cursor()
        if name is not None:
            cur.execute(f'''
            DELETE FROM {t_name} WHERE name = '{name}'
            ''')
        elif user_id is not None:
            cur.execute(f'''
            DELETE FROM {t_name} WHERE user_id = {user_id}
            ''')
    print(cur.fetchall())


if __name__ == '__main__':
    # create_table('users')
    # insert_data({'name': 'test', 'sex': 1, 'age': 1, 'score': 1})
    # update_data('users', 1, 'name', 'test2')
    # delete_user('users', 1, 'test')
    # drop_table('users')
