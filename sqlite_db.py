import sqlite3 as sq
import json
from files.dicts import dict_dicts


# Database

async def sql_start():
    global db, cursor
    db = sq.connect('users.db')
    cursor = db.cursor()
    if db:
        print('Database USERS succesfully started!;)')
    db.execute(
        "CREATE TABLE IF NOT EXISTS users(user_id TEXT PRIMARY KEY,username TEXT, name TEXT, progress TEXT, hw1 BOOLEAN, hw2 BOOLEAN, hw3 BOOLEAN, hw4 BOOLEAN, hw5 BOOLEAN, hw6 BOOLEAN, hw7 BOOLEAN,"
        " hw8 BOOLEAN, hw9 BOOLEAN, hw10 BOOLEAN, hw11 BOOLEAN, hw12 BOOLEAN, hw13 BOOLEAN, hw14 BOOLEAN, hw15 BOOLEAN, hw16 BOOLEAN, hw17 BOOLEAN, hw18 BOOLEAN,"
        " hw19 BOOLEAN, hw20 BOOLEAN, hw21 BOOLEAN, hw22 BOOLEAN, hw23 BOOLEAN, hw24 BOOLEAN, hw25 BOOLEAN, hw26 BOOLEAN, hw27 BOOLEAN, hw28 BOOLEAN, hw29 BOOLEAN, last_verb TEXT, level_verbs INTEGER, progress_verbs TEXT, last_sentence TEXT)")
    # db.execute("CREATE TABLE IF NOT EXISTS words(user_id TEXT PRIMARY KEY,username TEXT, name TEXT, progress TEXT,)")
    db.commit()


async def create_profile(user_id, username, name):
    user = cursor.execute("SELECT 1 FROM users WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cursor.execute(
            "INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, username, name, '[]', 'False', 'False', 'False', 'False', 'False', 'False', 'False', 'False',
             'False', 'False', 'False', 'False', 'False', 'False', 'False', 'False', 'False', 'False', 'False', 'False',
             'False', 'False', 'False', 'False', 'False', 'False', 'False', 'False', 'False', '[]', 1,
             '[]', '[]'))
        db.commit()


# async def create_profile_words(user_id, username, name):
#     user = cursor.execute("SELECT 1 FROM words WHERE user_id == '{key}'".format(key=user_id)).fetchone()
#     if not user:
#         cursor.execute(
#             "INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
#             (user_id, username, name, '[]', 'False', 'False',))


async def edit_hw_done(user_id, hw_name):
    cursor.execute(
        "UPDATE users SET '{}' = 'True' WHERE user_id == '{}'".format(hw_name, user_id))
    db.commit()


async def edit_hw_undone(user_id, hw_name):
    cursor.execute(
        "UPDATE users SET '{}' = 'False' WHERE user_id == '{}'".format(hw_name, user_id))
    db.commit()


async def get_progress(user_id):
    cursor.execute("SELECT progress FROM users WHERE user_id== ?", (user_id,))
    row = cursor.fetchone()
    if row is not None:
        list_as_text = row[0]
        my_list = json.loads(list_as_text)
        return my_list
    db.commit()


async def update_progress(user_id, data=[]):
    list_as_text = json.dumps(data)
    cursor.execute(
        "UPDATE users SET progress = ? WHERE user_id == ?", (list_as_text, user_id))
    db.commit()


async def get_last_sentence(user_id):
    cursor.execute("SELECT last_sentence FROM users WHERE user_id== ?", (user_id,))
    row = cursor.fetchone()
    if row is not None:
        list_as_text = row[0]
        my_list = json.loads(list_as_text)
        return my_list
    db.commit()


async def update_last_sentence(user_id, data=[]):
    try:
        str_as_text = json.dumps(data)
        cursor.execute(
            "UPDATE users SET last_sentence = ? WHERE user_id == ?", (str_as_text, user_id))
        db.commit()
    except:
        print(f'Ошибка в функции update_last_sentence\n{user_id}\n{data}')


async def check_hw(user_id):
    result = cursor.execute(
        "SELECT * FROM users WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if result:
        return (result.index('False') - 3)
    else:
        return None


async def get_users_dict():
    dict = {}
    cursor.execute("SELECT user_id, username, name FROM users")
    row = cursor.fetchall()
    for elem in row:
        dict[elem[0]] = f'{elem[0]}: {elem[2]}'
    return dict


async def see_user_hw_progress(user_id):
    result = cursor.execute(
        "SELECT * FROM users WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    progress = ''
    my_list = []
    if len(result[3]) > 2:
        my_list = json.loads(result[3])
    hw_number = result.index('False') - 3
    dct = dict_dicts[hw_number]
    if len(my_list) > 0:
        progress = f'Сейчас выполнено {len(my_list)} предложений из {len(dct)}\nв Д/З №{hw_number}\n\n'
    final_result = ''
    final_result = progress
    if len(result[-2]) > 2:
        verbs = json.loads(result[-2])
        final_result += f'Сейчас переведено {len(verbs)} слов из 120\nна уровне {result[-3]} \n\n'

    else:
        final_result += f'Сейчас переведено 0 слов из 120\nна уровне {result[-3]} \n\n'
    for i in range(1, 16):  ############## Здесь количество отображаемых ДЗ ################
        final_result += f"""ДЗ №{i}: {'✅Выполнено' if result[i + 3] == 'True' else '❌Не выполнено'}\n"""
    return final_result


########################### VERBS ###########################
async def get_progress_verbs(user_id):
    cursor.execute("SELECT progress_verbs FROM users WHERE user_id== ?", (user_id,))
    row = cursor.fetchone()
    if row is not None:
        list_as_text = row[0]
        my_list = json.loads(list_as_text)
        return my_list
    db.commit()


async def update_progress_verbs(user_id, data=[]):
    list_as_text = json.dumps(data)
    cursor.execute(
        "UPDATE users SET progress_verbs = ? WHERE user_id == ?", (list_as_text, user_id))
    db.commit()


async def get_or_edit_verbs_level(user_id, edited=False):
    if edited == False:
        cursor.execute("SELECT level_verbs FROM users WHERE user_id== ?", (user_id,))
        value = cursor.fetchone()[0]
        return value
        db.commit()
    elif edited == True:
        cursor.execute("SELECT level_verbs FROM users WHERE user_id== ?", (user_id,))
        value = cursor.fetchone()[0]
        value += 1
        cursor.execute(
            "UPDATE users SET level_verbs = ? WHERE user_id == ?", (value, user_id))
        return value
        db.commit()


async def get_last_verb(user_id):
    cursor.execute("SELECT last_verb FROM users WHERE user_id== ?", (user_id,))
    row = cursor.fetchone()
    if row is not None:
        list_as_text = row[0]
        my_list = json.loads(list_as_text)
        return my_list
    db.commit()


async def update_last_verb(user_id, data=[]):
    try:
        str_as_text = json.dumps(data)
        cursor.execute(
            "UPDATE users SET last_verb = ? WHERE user_id == ?", (str_as_text, user_id))
        db.commit()
    except:
        print(f'Ошибка в функции update_last_verb\n{user_id}\n{data}')


dict_hw = {
    1: 'hw1', 2: 'hw2', 3: 'hw3', 4: 'hw4', 5: 'hw5', 6: 'hw6', 7: 'hw7', 8: 'hw8', 9: 'hw9',
    10: 'hw10', 11: 'hw11', 12: 'hw12', 13: 'hw13', 14: 'hw14', 15: 'hw15', 16: 'hw16',
    17: 'hw17', 18: 'hw18', 19: 'hw19', 20: 'hw20', 21: 'hw21', 22: 'hw22', 23: 'hw23',
    24: 'hw24', 25: 'hw25', 26: 'hw26', 27: 'hw27', 28: 'hw28', 29: 'hw29'
}
