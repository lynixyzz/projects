from random import randint

"""
В названиях переменных/функций snake_case - стандарт. camelCase это больше JavaScript/Java
Рекурсия в функции - норм до поры до времени
минус - нет проверки на введенный номер, он может не входить в диапазон [1, 100]
"""


def greetings() -> None:
    """Приветствует пользователя, объясняя правила игры."""
    print(
        'Привет!\n'
        'Ты запустил игру. Её суть - угадать число от 1 до 100 включительно.\n'
        'Если не угадал - буду подсказывать: число больше или меньше твоего предположения.\n'
    )


def get_integer(text: str) -> int:
    """Получает от пользователя целое число в диапазоне [1, 100].

    При вводе значения, которое нельзя преобразовать в int или
    которое не принадлежит диапазону [1, 100],
    выводит сообщение об ошибке и повторяет запрос.

    Args:
        text (str): текст приглашения для ввода

    Returns:
        int: целое число, введённое пользователем
    """
    while True:
        try:
            integer = int(input(text).strip())

            if 1 <= integer <= 100:
                return integer

            print('Число должно быть от 1 до 100 включительно. Попробуй еще раз.\n')
        except ValueError:
            print('Нужно вводить целое число. Попробуй еще раз.\n')


def get_attempt_form(number: int) -> str:
    """На основе предоставленного числа выбирает правильную форму слову "попытка"."""
    if 11 <= number % 100 <= 14:
        return 'попыток'

    if number % 10 == 1:
        return 'попытка'

    if number % 10 in (2, 3, 4):
        return 'попытки'

    return 'попыток'


def game() -> None:
    """Начинает игру и доводит ее до конца."""
    mystery_number = randint(1, 100)
    attempt_number = 1
    user_try = get_integer('Я загадал число! Твоя первая попытка: ')

    while user_try != mystery_number:
        attempt_number += 1

        if user_try > mystery_number:
            print('Загаданное число меньше!\n')
        else:
            print('Загаданное число больше!\n')

        user_try = get_integer(f'{attempt_number}-я попытка: ')

    print(f'\nЗагаданное число - {mystery_number}. '
        f'Красавчик! Тебе потребовалось {attempt_number} {get_attempt_form(attempt_number)}.\n'
    )


if __name__ == '__main__':
    greetings()

    while True:
        game()

        while True:
            choice = input('Хорошая партия вышла. Повторим игру? (y/n): ').strip().lower()

            if choice in ('y', 'n'):
                break
                
            print('Введите "y" или "n".')

        if choice == 'n':
            print('Ну... В таком случае... До новых встреч!')
            break