import sqlite3


def max_id_from_db(connection: sqlite3.Connection) -> int:
    """Возвращает наибольшее значение из поля language_id.
    
    Args:
        connection (sqlite3.Connection): Соединение с базой данных SQLite.
    
    Returns:
        Наибольшее значение из поля language_id. Если значений в поле нет - 0.

    """
    return connection.execute('''
        SELECT COALESCE(MAX(language_id), 0)
        FROM languages
    ''').fetchone()[0]


def ask_for_int(
    minimum: int | None = None,
    maximum: int | None = None,
) -> int:
    """Просит у пользователя целое число на ввод с проверкой на вход
    в промежуток.

    
    Args:
        minimum (int): минимальное допустимое значение, 
            включительно. По умолчанию - None
        maximum (int): максимальное допустимое значение, 
            включительно. По умолчанию - None
    
    Returns:
        int: целое число, которе прошло все внутренние проверки
    """
    if minimum is not None and maximum is not None:
        if minimum > maximum:
            raise ValueError('Минимум не может быть больше максимума.')

    while True:
        try:
            value = int(input('Введите значение: '))
        except ValueError: # переписать нормально
            print('Введите целое число.\n')
            continue

        if (
            (minimum is None or value >= minimum)
            and
            (maximum is None or value <= maximum)
        ):
            return value

        if minimum is not None and maximum is not None:
            print(f'Введите значение от {minimum} до {maximum} включительно.\n')
        elif minimum is not None:
            print(f'Введите значение не меньше {minimum}.\n')
        elif maximum is not None:
            print(f'Введите значение не больше {maximum}.\n')


def ask_for_str(
    accepted_values: list[str] | None = None, 
    ignore_case: bool = True,
) -> str: # 
    """Просит у пользователя строку на ввод с проверкой на введенные значения.

    
    Args:
        accepted_values (list[str] | None): значения, доступные к вводу. По умолчанию - None
        ignore_case (bool): игнорировать ли регистр. По умолчанию - True
    
    Returns:
        str: строка, которая прошла все внутренние проверки
    """
    if accepted_values == []:
        raise ValueError('Список допустимых значений не может быть пустым.')
    
    visible_values = accepted_values

    if ignore_case is True and accepted_values is not None:
        accepted_values = [value.lower() for value in accepted_values]
    
    while True:
        if accepted_values is None:
            print('Введите: ', end='')
        else:
            print(f'Введите ({"/".join(visible_values)}): ', end='')

        value = input().strip()

        if ignore_case is True:
            value = value.lower()

        if accepted_values is None or value in accepted_values:
            return value

        print('Введите верное значение.\n')


def show_languages(connection: sqlite3.Connection) -> None:
    """Выводит список доступных языков из базы данных.

    Args:
        connection (sqlite3.Connection): соединение с базой данных,
            с которой будет браться список языков
    """
    languages = connection.execute(
        'SELECT language_id, name, alphabet FROM languages ORDER BY language_id'
    ).fetchall()

    for language_id, name, alphabet in languages:
        print(f'{language_id}. {name} - {alphabet}')