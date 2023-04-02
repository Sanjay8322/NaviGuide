import psycopg2


def connect_db():
    # TODO Move the db connection credentials to a .env file and load it from there
    conn = psycopg2.connect(
        database="naviguide",
        user="postgres",
        password="cool123!",
        host="localhost",
        port="5432"
    )
    return conn


def create_survey_table(conn):
    with conn.cursor() as cursor:
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS survey_responses (
                id SERIAL PRIMARY KEY,
                name TEXT,
                visit_purpose TEXT,
                visitor_status TEXT,
                first_time BOOLEAN,
                like_naviguide BOOLEAN,
                improve_feedback TEXT
            )
            '''
        )
        conn.commit()
