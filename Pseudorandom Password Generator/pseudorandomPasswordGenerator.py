import random
import string


def generate(
        lowercase: bool, 
        uppercase: bool, 
        punctuation: bool, 
        digits: bool, 
        length: int
        ) -> str:
    """Генерирует пароль по критериям из вводных данных."""
    if not (lowercase or uppercase or punctuation or digits):
        raise ValueError('Должна быть выбрана хотя бы одна категория символов')

    if length <= 0:
        raise ValueError('Длина не может быть меньше или равна нулю.')

    characters = ''

    if lowercase:
        characters += string.ascii_lowercase

    if uppercase:
        characters += string.ascii_uppercase

    if punctuation:
        characters += string.punctuation

    if digits:
        characters += string.digits

    return ''.join(random.choice(characters) for _ in range(length))


def get_password_options() -> tuple[bool, bool, bool, bool, int]:
    """Выводит главное меню и спрашивает пользователя о критериях пароля."""
    print('====================== PASSWORD GENERATOR ======================')
    print('  Выберите символы, из которых разрешено генерировать пароль:\n')
    print(f'1. {string.ascii_lowercase}')
    print(f'2. {string.ascii_uppercase}')
    print(f'3. {string.punctuation}')
    print(f'4. {string.digits}\n')

    choice = input('Вводите (формат ввода - 132...): ')

    while not all(char in '1234' for char in choice) or not choice:
        print('Введите только цифры от 1 до 4.\n')

        choice = input('Вводите (формат ввода - 132...): ')

    while True:
        try:
            length = int(input('Введите длину пароля: '))

            if length <= 0:
                print('Длина не может быть меньше или равна нулю.')
                continue

            break
        except ValueError:
            print('Введите ЦЕЛОЕ число.\n')

    return '1' in choice, '2' in choice, '3' in choice, '4' in choice, length


if __name__ == '__main__':
    lowercase, uppercase, punctuation, digits, length = get_password_options()

    print(f'\nВаш пароль: {generate(lowercase, uppercase, punctuation, digits, length)}')