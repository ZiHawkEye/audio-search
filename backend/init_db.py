import sqlite3
import os

def init_db():
    connection = sqlite3.connect('database.db')

    # Get the absolute path to schema.sql
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')

    with open(schema_path) as f:
        connection.executescript(f.read())

    cur = connection.cursor()

    connection.commit()
    connection.close()

init_db()