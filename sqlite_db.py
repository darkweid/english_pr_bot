import sqlite3 as sq
import json


# Database

async def sql_start():
    global db, cursor
    db = sq.connect('users.db')
    cursor = db.cursor()
    if db:
        print('Database succesfully started!;)')
    db.execute(
        "CREATE TABLE IF NOT EXISTS users(user_id TEXT PRIMARY KEY,username TEXT, name TEXT, progress TEXT, hw1 BOOLEAN, hw2 BOOLEAN, hw3 BOOLEAN, hw4 BOOLEAN, hw5 BOOLEAN, hw6 BOOLEAN, hw7 BOOLEAN,"
        " hw8 BOOLEAN, hw9 BOOLEAN, hw10 BOOLEAN, hw11 BOOLEAN, hw12 BOOLEAN, hw13 BOOLEAN, hw14 BOOLEAN, hw15 BOOLEAN, hw16 BOOLEAN, hw17 BOOLEAN, hw18 BOOLEAN,"
        " hw19 BOOLEAN, hw20 BOOLEAN, hw21 BOOLEAN, hw22 BOOLEAN, hw23 BOOLEAN, hw24 BOOLEAN, hw25 BOOLEAN, hw26 BOOLEAN, hw27 BOOLEAN, hw28 BOOLEAN, hw29 BOOLEAN, hw30 BOOLEAN, hw31 BOOLEAN, hw32 BOOLEAN)")
    db.commit()


async def create_profile(user_id, username, name):
    user = cursor.execute("SELECT 1 FROM users WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cursor.execute(
            "INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, username, name, 'None', 'False', 'False', 'False', 'False', 'False', 'False', 'False', 'False',
             'False', 'False', 'False', 'False', 'False', 'False', 'False', 'False', 'False', 'False', 'False', 'False',
             'False', 'False', 'False', 'False', 'False', 'False', 'False', 'False', 'False', 'False', 'False',
             'False',))
        db.commit()


async def edit_profile(state, user_id):
    async with state.proxy() as data:
        cursor.execute(
            "UPDATE profile SET photo = '{}', age = '{}', description = '{}', name = '{}' WHERE user_id == '{}'".format(
                data['photo'], data['age'], data['description'], data['name'], user_id))
        db.commit()


async def edit_hw_done(user_id, hw_name):
    cursor.execute(
        "UPDATE users SET '{}' = 'True' WHERE user_id == '{}'".format(hw_name, user_id))
    db.commit()


async def get_progress(user_id):
    cursor.execute("SELECT progress FROM users WHERE user_id=='{}'".format(user_id))
    row = cursor.fetchone()
    if row is not None:
        list_as_text = row[0]
        my_list = json.loads(list_as_text)
        return my_list
    db.commit()


async def update_progress(user_id, data=[]):
    list_as_text = json.dumps(data)
    cursor.execute(
        "UPDATE users SET progress = '{}' WHERE user_id == '{}'".format(list_as_text, user_id))
    db.commit()


async def check_hw(user_id):
    result = cursor.execute(
        "SELECT * FROM users WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if result:
        return (result.index('False') - 3)
    else:
        return None

async def get_users_list():
    cursor.execute("SELECT user_id, username, name FROM users")
    row = cursor.fetchone()
    print(row)


dict_hw = {
    1: 'hw1', 2: 'hw2', 3: 'hw3', 4: 'hw4', 5: 'hw5', 6: 'hw6', 7: 'hw7', 8: 'hw8', 9: 'hw9',
    10: 'hw10', 11: 'hw11', 12: 'hw12', 13: 'hw13', 14: 'hw14', 15: 'hw15', 16: 'hw16',
    17: 'hw17', 18: 'hw18', 19: 'hw19', 20: 'hw20', 21: 'hw21', 22: 'hw22', 23: 'hw23',
    24: 'hw24', 25: 'hw25', 26: 'hw26', 27: 'hw27', 28: 'hw28', 29: 'hw29', 30: 'hw30',
    31: 'hw31', 32: 'hw32'
}
