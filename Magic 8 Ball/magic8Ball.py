import random
import json
import pathlib


def get_name(text: str) -> str:
    """Возвращает пользовательский ввод, если он проходит проверку на пустоту.
    
    Args:
        text: текст для поля input() при пользовательском вводе
    
    Returns:
        str: непустое имя без лишних пробелов
    """
    name = input(text).strip()
    
    while not name:
        print('Имя не может быть пустым!\n')
        name = input(text).strip()

    return name


def confirm_name(name: str) -> str:
        """Переспрашивает пользователя о его имени для
        перезаписи в случае ошибочного ввода.

        Args:
            name: *имя*, на основе которого будет само уточнение по имени (вас зовут {*имя*}?)
        """
        while True:
            choice = input(f'Вас зовут {name}? (y/n): ').strip().lower()
                    
            if choice == 'n':
                name = get_name('Введите свое имя: ')
                continue

            if choice == 'y':
                return name

            print('Введите "y" или "n".\n') 


def load_data() -> tuple[str, dict]:
    """Экспортирует имя пользователя и фразы с файлов.
    Если файла с именем нет, то создает его, записывая введенное имя.

    Returns:
        name: имя пользователя
        phrases: фразы с файла phrases.json
    """
    current_dir = pathlib.Path(__file__).parent
    phrases_path = current_dir / 'phrases.json'
    name_path = current_dir / 'name.txt'
    phrases = json.loads(phrases_path.read_text(encoding='utf-8'))

    if name_path.exists():
        name = name_path.read_text(encoding='utf-8').strip()
        name = confirm_name(name)
    else:
        name = get_name('Введите свое имя: ')
        name = confirm_name(name)

    name_path.write_text(name, encoding='utf-8')

    return name, phrases


def main() -> None:
    """Основная логика программы."""
    name, phrases = load_data()

    input(
        f'\nПривет, {name}. Я - магический шар, знаю ответы на ВСЕ вопросы. '
        'Что тебя интересует?\n'
        'Вопрос: '
    )
    
    category = phrases[random.choice(list(phrases))]
    answer = random.choice(category)

    print()
    print(answer)

if __name__ == '__main__':
    main()