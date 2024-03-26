import psycopg2


def createdb()-> None:
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        user='note',
        password='1234',
        dbname='finalproject'
    )
    with conn.cursor() as cursor:
        cursor.execute("""

CREATE TABLE question (
    id BIGSERIAL PRIMARY KEY,
    question_text VARCHAR(255) NOT NULL
);

CREATE TABLE choice (
    id BIGSERIAL PRIMARY KEY,
    choice_text VARCHAR(255) NOT NULL,
    votes INTEGER,
    question_id BIGINT NOT NULL REFERENCES question(id)
);

CREATE TABLE user_stat (
    id BIGSERIAL PRIMARY KEY,
    tg_user_id BIGINT NOT NULL,
    question_id BIGINT NOT NULL REFERENCES question(id),
    choice_id BIGINT NOT NULL REFERENCES choice(id)
);

        """)
        conn.commit()
    conn.close
def get_user_stat():
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        user='note',
        password='1234',
        dbname='finalproject'
    )
    with conn.cursor() as cursor:
        cursor.execute("""SELECT * FROM user_stat""")
        all_records=cursor.fetchall()
        print (str(all_records))
        conn.commit()
    conn.close()
    return str(all_records)

def save_question(question_text:str ):
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        user='note',
        password='1234',
        dbname='finalproject'
    )
    with conn.cursor() as cursor:
        cursor.execute("""INSERT INTO question (question_text) VALUES (%s)""", (question_text, ))
        conn.commit()
        conn.close()
def save_answer(answers:str, question_id:int ):
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        user='note',
        password='1234',
        dbname='finalproject'
    )
    with conn.cursor() as cursor:
        cursor.execute("""INSERT INTO choice (choice_text, question_id) VALUES (%s, %s)""", (answers, question_id ))
        conn.commit()
        conn.close()
def get_question():
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        user='note',
        password='1234',
        dbname='finalproject'
    )
    with conn.cursor() as cursor:
        cursor.execute("""SELECT * FROM question""")
        all_records=cursor.fetchall()
        print (str(all_records))
        conn.commit()
    conn.close()
    return str(all_records)

def delete_questions(number:int):
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        user='note',
        password='1234',
        dbname='test'
    )
    with conn.cursor() as cursor:
        cursor.execute("""DELETE FROM question WHERE id=(%s);
        DELETE FROM choice WHERE question_id=(%s);
        DELETE FROM user_stat WHERE question_id=(%s)""", (number, ))
        conn.commit()
    conn.close()

if __name__=='__main__':
    save_answer('lf', 1)
    save_question('eubwdh?')
