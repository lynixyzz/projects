import pathlib
import sqlite3
import subprocess
import string
import sys
from misc import ask_for_int, show_languages, ask_for_str, max_id_from_db


def choose_alphabet(connection: sqlite3.Connection) -> str:
    """Запрашивает ID языка из представленных значений и выводит его алфавит.

    Есть возможность настройки языков.

    Args:
        connection (sqlite3.Connection): Соединение с базой данных SQLite.

    Returns:
        str: Алфавит выбранного языка.
    """
    while True:
        additional_id = max_id_from_db(connection) + 1

        print('\n' * 12)
        show_languages(connection)
        print(f'{additional_id}. Настроить языки...\n')

        choice = ask_for_int(1, additional_id)

        if choice == additional_id:
            script_dir = pathlib.Path(__file__).parent
            language_configurator_path = script_dir / 'languageConfigurator.py'

            subprocess.run(
                [sys.executable, language_configurator_path],
                check=True,
            )
        else:
            break

    alphabet = connection.execute(
        'SELECT alphabet FROM languages WHERE language_id = ?',
        (choice,)
    ).fetchone()[0]

    return alphabet


def decryptor(encrypted_string: str, alphabet: str, shift: int) -> None:
    """Расшифровывает зашифрованное шифром Цезаря сообщение.
    
    Args:
        encrypted_string (str): Зашифрованная строка, которая будет расшифровываться.
        alphabet (str): Алфавит, на котором написана зашифрованная строка.
        shift (int): Сдвиг.
    """
    upper_alphabet = alphabet.upper()
    lower_alphabet = alphabet.lower()
    punctuation = string.punctuation + '«»—…'

    for char in encrypted_string:
        if char in punctuation or char.isspace():
            print(char, end='', flush=True)
            continue

        decryption_alphabet = (
            upper_alphabet if char.isupper() else lower_alphabet
        )
        
        decrypted_index = (decryption_alphabet.index(char) - shift) % len(decryption_alphabet)

        print(decryption_alphabet[decrypted_index], end='', flush=True)
    
    print()


def encryptor(original_string: str, alphabet: str, shift: int) -> None:
    """Зашифровывает шифром Цезаря сообщение.
        
    Args:
        original_string (str): Строка, которая будет зашифрована.
        alphabet (str): Алфавит, на котором написана оригинальная строка.
        shift (int): Сдвиг.
    """
    upper_alphabet = alphabet.upper()
    lower_alphabet = alphabet.lower()
    punctuation = string.punctuation + '«»—…'

    for char in original_string:
        if char in punctuation or char.isspace():
            print(char, end='', flush=True)
            continue

        decryption_alphabet = (
            upper_alphabet if char.isupper() else lower_alphabet
        )
        
        decrypted_index = (decryption_alphabet.index(char) + shift) % len(decryption_alphabet)

        print(decryption_alphabet[decrypted_index], end='', flush=True)
    
    print()


def is_alphabetic(alphabet: str, string_for_check: str) -> bool:
    """Проверяет, что каждый символ строки есть в 
    алфавите либо является разрешённым знаком (пунктуация, пробелы).
    
    Args:
        alphabet (str): Алфавит, относительно которого будет идти проверка.
        string_for_check (str): Строка, которая проверяется.
    """
    allowed_letters = alphabet.lower()

    for letter in string_for_check.lower():
        if (
            (letter not in allowed_letters)
            and
            (letter not in string.punctuation)
            and 
            (letter not in ('»', '«', '—', '…'))
            and
            (not letter.isspace())
        ):
            return False

    return True


def main_logic(connection: sqlite3.Connection) -> None:
    """Показывает главное меню и выполняет одно выбранное действие
    с последующим запросом данных, где это необходимо.
    
    Args:
        connection (sqlite3.Connection): Соединение с базой данных SQLite.

    Raises:
        SystemExit: Если пользователь выбрал пункт "Выйти".
    """
    print('\n' * 12)
    print('====================== DECRYPTOR/ENCRYPTOR ======================')
    print(' 1. Зашифровать (положительный сдвиг)')
    print(' 2. Расшифровать (отрицательный сдвиг)')
    print(' 3. Выйти\n')

    choice = ask_for_int(1, 3)

    if choice in (1, 2):
        alphabet = choose_alphabet(connection)

        print('\nУкажите сдвиг.')
        shift = ask_for_int(1, None)
        
        print('\nВведите текст, над которой будет проводиться операция.')
        while True:
            string = ask_for_str(None, False)
        
            if is_alphabetic(alphabet, string):
                break
        
            print('В введенной строке есть значения не из алфавита.\n')

        print('\nРезультат: ', end='')

        if choice == 1:
            encryptor(string, alphabet, shift)
        elif choice == 2:
            decryptor(string, alphabet, shift)
    elif choice == 3:
        raise SystemExit


if __name__ == '__main__':
    script_dir = pathlib.Path(__file__).parent
    db_path = script_dir / 'languages.db'

    connection = sqlite3.connect(db_path)

    main_logic(connection)