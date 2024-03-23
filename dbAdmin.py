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
    votes INTEGER NOT NULL,
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
        cursor.execute(""""INSERT INTO question VALUES (%s)""", (question_text, ))
        conn.commit()
        conn.close()



if __name__=='__main__':
    save_question('eubwdh?')