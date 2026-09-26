import sqlite3
import pathlib

print(f'Версия SQLite: {sqlite3.sqlite_version}')

script_dir = pathlib.Path(__file__).parent
db_path = script_dir / 'languages.db'

default_data = [
    (1, 'Русский без Ё (Russian)', 'абвгдежзийклмнопрстуфхцчшщъыьэюя'),
    (2, 'Русский с Ё (Russian)', 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'),
    (3, 'English', 'abcdefghijklmnopqrstuvwxyz')
]

with sqlite3.connect(db_path) as connection:
    connection.execute("DROP TABLE IF EXISTS languages")

    connection.execute("""
        CREATE TABLE languages (
            language_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            alphabet TEXT NOT NULL
        )
    """)

    connection.executemany(
        'INSERT INTO languages (language_id, name, alphabet) VALUES (?, ?, ?)',
        default_data
    )

print(f'База данных создана: {db_path}')