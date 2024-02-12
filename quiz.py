import sqlite3
from random import randint



db_name = 'quiz.sqlite'
conn = None
cursor = None


def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()


def do(query):
    cursor.execute(query)
    conn.commit()


def create():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    do('''CREATE TABLE IF NOT EXISTS quiz (id INTEGER PRIMARY KEY, name VARCHAR)''')
    do('''CREATE TABLE IF NOT EXISTS question (id INTEGER PRIMARY KEY, question VARCHAR, answer VARCHAR, 
    wrong1 VARCHAR, wrong2 VARCHAR, wrong3 VARCHAR )''')
    do('''CREATE TABLE IF NOT EXISTS quiz_content (id INTEGER PRIMARY KEY, 
                                             quiz_id INTEGER,
                                             question_id INTEGER,
                                             FOREIGN KEY (quiz_id) REFERENCES quiz (id),
           FOREIGN KEY (question_id) REFERENCES question (id))''')
    close()


def close():
    cursor.close()
    conn.close()


def clear():
    open()
    do('''DROP TABLE IF EXISTS question''')
    do('''DROP TABLE IF EXISTS quiz''')
    do('''DROP TABLE IF EXISTS quiz_content''')
    close()


def add_questions():
    questions = [
        ('Сколько дней в неделe?', '7', '4', '5', '6'),
        ('Какой самый знаменитый програмист в мире?', 'Линус Торвальдс', 'Джеймс Гослинг', 'Гвидо ван Россум',
         'Бьерн Страуструп'),
        ('Самый посещаемый сайт в мире', 'google.com', 'twitter.com.', 'facebook.com.', 'youtube.com')

    ]
    open()
    cursor.executemany('''INSERT INTO question (question, answer, wrong1,wrong2,wrong3) VALUES (?,?,?,?,?)''', questions)
    conn.commit()
    close()

def add_quiz():
    quizes = [
        ('Своя игра', ),
        ('Кто хочет стать богатым на 2 года', ),
        ('Гений ты или нет?', )
    ]
    open()
    cursor.executemany('''INSERT INTO quiz (name) VALUES (?)''', quizes)
    conn.commit()
    close()
def add_links():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')

    answer = input('Добавить связь? y/n')
    while answer != 'n':
        quiz_id = int(input('id викторины'))
        question_id = int(input('id вопроса'))
        cursor.execute('''INSERT INTO quiz_content (quiz_id, question_id) VALUES (?,?)''', [quiz_id, question_id])
        conn.commit()
        answer = input('Добавить связь y/n')
    close()

def show_tables():
    open()
    cursor.execute('''SELECT * FROM quiz''')
    print(cursor.fetchall())
    cursor.execute('''SELECT * FROM quiz_content''')
    print(cursor.fetchall())
    cursor.execute('''SELECT * FROM question''')
    print(cursor.fetchall())
    close()
def get_question_after(question_id=0, quiz_id=1):
    open()
    cursor.execute('''SELECT quiz_content.id, question.question, question.answer, question.wrong1, question.wrong2, question.wrong3 FROM quiz_content, question WHERE quiz_content.question_id == question_id AND quiz_content.id > ? AND quiz_content.quiz_id == ? ORDER BY quiz_content.id''', [question_id, quiz_id])
    result = cursor.fetchone()
    close()
    return result



def get_quises():
    query = 'SELECT * FROM quiz ORDER BY id'
    open()
    cursor.execute(query)
    result = cursor.fetchall()
    close()
    return result
def get_question_id():
    query = 'SELECT quiz_id FROM quiz_content'
    open()
    cursor.execute(query)
    ids = cursor.fetchall()
    rand_num = randint(0, len(ids) - 1)
    rand_id = ids[rand_num][0]
    close()
    return rand_id

def check_answer(q_id, ans_text):
    query = '''SELECT question.answer FROM quiz_content, question WHERE quiz_content.id = ? AND quiz_content.question_id = question_id'''
    open()
    cursor.execute(query, str(q_id))
    result = cursor.fetchall()
    close()
    if result is None:
        return False
    else:
        if result[0] == ans_text:
            return True
        return False



def main():
    clear()
    create()
    add_questions()
    add_quiz()
    add_links()
    show_tables()
    print(get_question_after(2,1))

if __name__ == 'main':
    main()
    