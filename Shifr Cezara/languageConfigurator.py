import pathlib
import sqlite3
from misc import show_languages, ask_for_int, ask_for_str, max_id_from_db


def no_duplicates_check(string: str) -> bool:
    """Проверяет строку на уникальность символов без учета регистра.

    Args:
        string (str): Проверяемая строка.

    Returns:
        bool: True, если повторяющихся символов нет, иначе False.
    """
    seen = set()

    for char in string.lower():
        if char in seen:
            return False

        seen.add(char)

    return True


def add_language_db(
    connection: sqlite3.Connection, 
    alphabet: str, 
    name: str,
) -> None:
    """Добавляет язык в базу данных с языками.
    
    Args:
        connection: соединение sqlite
        alphabet: алфавит языка
        name: название языка
    """
    if no_duplicates_check(alphabet) == False:
        raise ValueError('Алфавит не должен содержать дубликатов.')

    connection.execute(
        'INSERT INTO languages (name, alphabet) VALUES (?, ?)',
        (name, alphabet),
    )

    connection.commit()


def remove_language_db(
    connection: sqlite3.Connection, 
    language_id: int,
) -> None:
    """Удаляет запись о конкретном языке.
    
    Args: 
        connection: соединение sqlite
        language_id: ID языка удаляемой строки
    """

    cursor = connection.execute(
        'DELETE FROM languages WHERE language_id = ?',
        (language_id,),
    )

    if cursor.rowcount == 0:
        print('Язык не найден.')
        return


    connection.execute(
        'UPDATE languages SET language_id = language_id - 1 WHERE language_id > ?',
        (language_id,),
    )

    connection.commit()


def edit_language_db(
    connection: sqlite3.Connection,
    language_id: int,
    name: str | None = None,
    alphabet: str | None = None,
) -> None:
    """Изменяет некоторые значения записи о конкретном языке.

    Args:
        connection (sqlite3.Connection): соединение sqlite
        language_id (int): порядковый номер изменяемой строки
        name (str, optional): имя языка, на которое изменить текущий: по умолчанию None
        alphabet (str, optional): алфавит языка, на которое изменить текущий: по умолчанию None
    """
    fields = []
    field_values = []

    if name is not None:
        fields.append('name = ?')
        field_values.append(name)

    if alphabet is not None:
        fields.append('alphabet = ?')
        field_values.append(alphabet)

    if alphabet is None and name is None:
        return

    sql = f"UPDATE languages SET {', '.join(fields)} WHERE language_id = ?"

    cursor = connection.execute(
        sql,
        (*field_values, language_id),
    )

    if cursor.rowcount == 0:
        print('Язык не найден.')
        return

    connection.commit()


def add_language_from_menu(connection: sqlite3.Connection) -> None:
    """Запрашивает данные языка и добавляет его в базу данных.

    Повторяет ввод названия и алфавита, пока пользователь не подтвердит
    их ответом "y".

    Args:
        connection (sqlite3.Connection): Соединение с базой данных SQLite.
""" 
    while True:
        print('\nВведите название языка.')
        name = ask_for_str(None, False)
        if name == '':
            print('Введите корректное название.')
            continue

        print('\nВведите алфавит.')
        alphabet = ask_for_str(None, True)
        if alphabet == '':
            print('Введите корректное название.')
            continue

        while no_duplicates_check(alphabet) == False:
            print('Каждый символ алфавита должен быть уникален.')

            print('\nВведите алфавит.')
            alphabet = ask_for_str(None, True)

        print('\n-----------------------------------')

        print(f'\nНазвание: {name}')
        print(f'Алфавит: {alphabet}')
        print('Верно?')

        choice = ask_for_str(['y', 'n'], True)

        if choice == 'y':
            break

    add_language_db(connection, alphabet, name)


def remove_language_from_menu(connection: sqlite3.Connection) -> None:
    """Запрашивает данные языка и удаляет его из базы данных.

    Повторяет ввод ID для удаления, пока пользователь не подтвердит
    его ответом "y".

    Args:
        connection (sqlite3.Connection): Соединение с базой данных SQLite.
    """
    print()
    show_languages(connection)

    max_id = max_id_from_db(connection)

    if max_id == 0:
        print('Список языков пуст.')
        return

    while True:
        print('\nВведите ID языка для удаления.')
        language_id = ask_for_int(1, max_id)    
        print(f'\nID выбранного языка: {language_id}')
        print('Верно?')

        choice = ask_for_str(['y', 'n'], True)
    
        if choice == 'y':
            break

    remove_language_db(connection, language_id)


def edit_language_from_menu(connection: sqlite3.Connection) -> None:
    """Запрашивает данные языка и изменяет выбранные данные в базе данных.

    Повторяет ввод изменяемых данных, пока пользователь не подтвердит
    его ответом "y".

    Args:
        connection (sqlite3.Connection): Соединение с базой данных SQLite.
    """
    print()
    show_languages(connection)

    max_id = max_id_from_db(connection)

    if max_id == 0:
        print('Список языков пуст.')
        return

    print('\nУкажите ID изменяемого языка.')
    language_id = ask_for_int(1, max_id)

    print('\nИзменить название?')
    name_needed = ask_for_str(['y', 'n'], True)

    print('\nИзменить алфавит?')
    alphabet_needed = ask_for_str(['y', 'n'], True)

    name = None
    alphabet = None

    if name_needed == 'y':
        print('\nУкажите новое имя.')
        name = ask_for_str(None, False)
        
    if alphabet_needed == 'y':
        print('\nУкажите новый алфавит.')
        alphabet = ask_for_str(None, True)

    edit_language_db(connection, language_id, name, alphabet)


def main_logic(connection: sqlite3.Connection) -> None:
    """Показывает главное меню и выполняет одно выбранное действие.
    
    Args:
        connection (sqlite3.Connection): Соединение с базой данных SQLite.

    Raises:
        SystemExit: Если пользователь выбрал пункт "Выйти".
    """
    print()
    print('====================== Language Configurator ======================')
    print(' Шифровка/расшифровка происходит относительно алфавитного ряда')
    print(' формата "abcde...xyz".\n')

    print(' 1. Добавить язык')
    print(' 2. Удалить язык')
    print(' 3. Изменить язык')
    print(' 4. Выйти\n')

    choice = ask_for_int(1, 4)

    if choice == 1:
        print('\n' * 12)
        add_language_from_menu(connection)
    elif choice == 2:
        print('\n' * 12)
        remove_language_from_menu(connection)
    elif choice == 3:
        print('\n' * 12)
        edit_language_from_menu(connection)
    elif choice == 4:
        raise SystemExit


if __name__ == '__main__':
    script_dir = pathlib.Path(__file__).parent
    db_path = script_dir / 'languages.db'

    connection = sqlite3.connect(db_path)

    while True:
        print('\n' * 12)
        main_logic(connection)