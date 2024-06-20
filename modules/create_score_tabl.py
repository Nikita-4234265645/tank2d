import sqlite3

def create_score_table():
    conn = sqlite3.connect('db4.sqlite3')

    create_table_query = """
    CREATE TABLE IF NOT EXISTS "players" (
     id INT PRIMARY KEY,
     nickname VARCHAR(100) NOT NULL, 
     score VARCHAR(50)
     )
    """

    conn.execute(create_table_query)
    conn.close()