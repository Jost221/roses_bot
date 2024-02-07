import sqlite3
import global_data


def create_table():
    connection = sqlite3.connect('Users.db')
    cursor = connection.cursor()

    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        telephone INTEGER,
        purchase_consent INTEGER,
        amount_transfers INTEGER DEFAULT 0,
        status INTEGER NOT NULL
    );
                   
    CREATE TABLE IF NOT EXISTS Bank (
        user_id INTEGER,
        bank_data INTEGER,
        bank_name TEXt,
        FOREIGN KEY(user_id) REFERENCES Users(id)
    );
    ''')

    connection.commit()
    connection.close()


def create_user(user_id):
    if get_status(user_id) != None:
        return "Вы уже зарегистрированны в системе"

    connection = sqlite3.connect('Users.db')
    cursor = connection.cursor()

    cursor.execute(
        '''INSERT INTO Users (
            user_id,
            status
        ) VALUES (?, ?)''',
        (user_id, 0)
    )

    connection.commit()
    connection.close()

def create_bank(user_id):
    connection = sqlite3.connect('Users.db')
    cursor = connection.cursor()

    cursor.execute(
        '''INSERT INTO bank (
            user_id,
        ) VALUES (?)''',
        (user_id)
    )

    connection.commit()
    connection.close()


def get_status(user_id):
    connection = sqlite3.connect('Users.db')
    cursor = connection.cursor()
    cursor.execute(
        f'''
        SELECT status FROM Users
        WHERE user_id = {user_id}
        '''
    )
    status = cursor.fetchall()
    connection.commit()
    connection.close()
    if len(status) == 0:
        return None
    return status[0][0]


def update_status(user_id, input_value, status):

    if status == 2 and input_value.lower() == 'да':
        creata_bank(user_id)
        new_status = status + 3

    else:
        new_status = status + 1

    connection = sqlite3.connect('Users.db')
    cursor = connection.cursor()

    if status < 3:
        cursor.execute(
            f'''
            UPDATE {global_data.first_data[status][2]} 
            SET status = ?, 
            {global_data.first_data[status][1]} = ? 
            WHERE user_id = ?
            ''',
            (new_status, input_value, user_id)
        )

        
    else:
        cursor.execute(
            f'''
            UPDATE {global_data.first_data[status][2]} 
            {global_data.first_data[status][1]} = ? 
            WHERE user_id = ?
            ''',
            (input_value, user_id)
        )

    connection.commit()
    connection.close()
    return new_status


def creata_bank(user_id):
    pass
