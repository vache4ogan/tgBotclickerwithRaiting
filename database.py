import sqlite3

connection = None
cursor = None


def init():
    global connection
    global cursor
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users
    (
    Id INTEGER PRIMARY KEY,
    UserName TEXT NOT NULL,
    Score INTEGER
    )
    ''')


def insert(user_id, User_Name, Score):
    try:
        cursor.execute('INSERT INTO Users (Id, UserName, Score) VALUES (?, ?, ?)', (user_id, User_Name, Score))
    except:
        print("Ошибка")


def update_score(score_updt, user_id):
    cursor.execute('UPDATE Users SET Score = ? WHERE Id = ?', (score_updt, user_id))


def delete(user_id):
    cursor.execute('DELETE FROM Users WHERE Id = ?', (user_id,))


def score_show(user_id):
    all = f"""SELECT * from Users WHERE Id = ?"""
    cursor.execute(all, (user_id,))
    all1 = cursor.fetchall()
    for row in all1:
        print(row[0])
        print(row[1])
        print(row[2])
        score = row[2]
    return score

def knowtop1(Score):
    all = f"""SELECT * from Users WHERE Score = ?"""
    cursor.execute(all, (Score, ))
    all1 = cursor.fetchall()
    for row in all1:
        print(row[0])
        print(row[1])
        print(row[2])
        Name = row[1]
    return Name

def rait_show():
    all = f"""SELECT * from Users"""
    cursor.execute(all)
    all1 = cursor.fetchall()
    return all1

def check(user_id):
    all = f"""SELECT Id from Users"""
    cursor.execute(all)
    all1 = cursor.fetchall()
    print(all1)
    if user_id in all1:
        return False
    elif user_id not in all1:
        return True


def commit():
    global connection
    connection.commit()


def close():
    global connection
    connection.close()
