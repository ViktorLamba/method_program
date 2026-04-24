import re


def validate_login(login: str) -> bool:
    """
    Валидация логина.
    Критерии:
    - Начинается с буквы
    - Содержит только латиницу, цифры и _
    - Длина 5-20 символов
    - Не может заканчиваться _
    """
    pattern = r'^[a-zA-Z][a-zA-Z0-9_]{4,19}(?<!_)$'
    return bool(re.fullmatch(pattern, login))


def find_dates(text: str) -> list:
    """
    Поиск дат в тексте.
    Форматы:
    - DD.MM.YYYY
    - DD-MM-YYYY
    - DD/MM/YYYY
    Дата и месяц: 1-2 цифры, год: 2 или 4 цифры
    """
    pattern = r'\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b'
    dates = re.findall(pattern, text)
    return dates


def parse_log(log_line: str) -> dict:
    """
    Парсинг логов.
    Формат: 2024-02-10 14:23:01 INFO user=ada action=login ip=192.168.1.15
    """
    pattern = r'^(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+\w+\s+user=(\w+)\s+action=(\w+)\s+ip=([\d.]+)$'
    match = re.match(pattern, log_line)

    if match:
        return {
            'date': match.group(1),
            'time': match.group(2),
            'user': match.group(3),
            'action': match.group(4),
            'ip': match.group(5)
        }
    return {}


def validate_password(password: str) -> bool:
    """
    Проверка пароля.
    Критерии:
    - Минимум 8 символов
    - Хотя бы одна заглавная буква
    - Хотя бы одна строчная буква
    - Хотя бы одна цифра
    - Хотя бы один спецсимвол !@#$%^&*
    """
    # Проверка длины
    if len(password) < 8:
        return False

    # Проверка наличия заглавной буквы
    if not re.search(r'[A-Z]', password):
        return False

    # Проверка наличия строчной буквы
    if not re.search(r'[a-z]', password):
        return False

    # Проверка наличия цифры
    if not re.search(r'\d', password):
        return False

    # Проверка наличия спецсимвола
    if not re.search(r'[!@#$%^&*]', password):
        return False

    # Проверка на отсутствие недопустимых символов
    if re.search(r'[^A-Za-z0-9!@#$%^&*]', password):
        return False

    return True


def validate_email_with_domains(email: str, domains: list) -> bool:
    """
    Валидация email с ограниченными доменами.
    Проверяет общий формат email и допустимость домена.
    """
    # Основной паттерн для email
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if not re.match(email_pattern, email):
        return False

    # Извлекаем домен из email
    match = re.search(r'@(.+)$', email)
    if not match:
        return False

    email_domain = match.group(1)

    # Проверяем, есть ли домен в списке допустимых
    return email_domain in domains


def normalize_phone(phone: str) -> str:
    """
    Нормализация телефонных номеров.
    Возвращает номер в формате +79991234567.
    """
    # Удаляем все нецифровые символы, кроме возможного плюса в начале
    cleaned = re.sub(r'[^\d+]', '', phone)

    # Если номер начинается с 8, меняем на +7
    if cleaned.startswith('8'):
        cleaned = '+7' + cleaned[1:]
    # Если номер начинается с 7, добавляем +
    elif cleaned.startswith('7'):
        cleaned = '+' + cleaned
    # Если номер начинается без кода страны, добавляем +7
    elif len(cleaned) == 10:
        cleaned = '+7' + cleaned
    # Если начинается с +, оставляем как есть
    elif not cleaned.startswith('+'):
        cleaned = '+7' + cleaned

    # Проверяем длину номера (должно быть 12 символов: + и 11 цифр)
    if len(cleaned) != 12:
        return ""  # или можно выбрасывать исключение

    return cleaned


if __name__ == "__main__":
    # Тест 1: Валидация логина
    print("Тест 1 - Валидация логина:")
    test_logins = [
        ("User123", True),      # валидный
        ("user_123", True),     # валидный
        ("123user", False),     # начинается с цифры
        ("us", False),          # слишком короткий
        ("user_", False),       # заканчивается на _
        ("user@name", False),   # содержит недопустимый символ
        ("VeryLongUsernameThatIsTooLong", False),  # слишком длинный
    ]

    for login, expected in test_logins:
        result = validate_login(login)
        status = "✓" if result == expected else "✗"
        print(f"{status} {login:30} -> {result} (expected: {expected})")

    print("\n" + "="*50 + "\n")

    # Тест 2: Поиск дат в тексте
    print("Тест 2 - Поиск дат в тексте:")
    text = "События произошли 12.03.2023 и 1-1-23, также 05/12/2024 и 31.12.99"
    dates = find_dates(text)
    print(f"Текст: {text}")
    print(f"Найденные даты: {dates}")

    print("\n" + "="*50 + "\n")

    # Тест 3: Парсинг логов
    print("Тест 3 - Парсинг логов:")
    log_line = "2024-02-10 14:23:01 INFO user=ada action=login ip=192.168.1.15"
    parsed = parse_log(log_line)
    print(f"Лог: {log_line}")
    print(f"Результат: {parsed}")

    print("\n" + "="*50 + "\n")

    # Тест 4: Проверка пароля
    print("Тест 4 - Проверка пароля:")
    test_passwords = [
        ("Pass123!", True),         # валидный
        ("password", False),        # нет заглавных, цифр, спецсимволов
        ("PASSWORD1!", False),      # нет строчных
        ("Password!", False),       # нет цифр
        ("Password123", False),     # нет спецсимволов
        ("Pass1!", False),          # слишком короткий
        ("Пароль123!", False),      # кириллица
        ("ValidPass123!@#", True),  # валидный с несколькими спецсимволами
    ]

    for pwd, expected in test_passwords:
        result = validate_password(pwd)
        status = "✓" if result == expected else "✗"
        print(f"{status} {pwd:20} -> {result} (expected: {expected})")

    print("\n" + "="*50 + "\n")

    # Тест 5: E-mail с ограниченными доменами
    print("Тест 5 - E-mail с ограниченными доменами:")
    domains = ['gmail.com', 'yandex.ru', 'edu.ru']
    test_emails = [
        ("user@gmail.com", True),
        ("test@yandex.ru", True),
        ("student@edu.ru", True),
        ("invalid@mail.ru", False),
        ("bad-email", False),
        ("user@yandex", False),
        ("@gmail.com", False),
    ]

    for email, expected in test_emails:
        result = validate_email_with_domains(email, domains)
        status = "✓" if result == expected else "✗"
        print(f"{status} {email:20} -> {result} (expected: {expected})")

    print("\n" + "="*50 + "\n")

    # Тест 6: Нормализация телефонных номеров
    print("Тест 6 - Нормализация телефонных номеров:")
    test_phones = [
        ("8 (999) 123-45-67", "+79991234567"),
        ("+7 999 123 45 67", "+79991234567"),
        ("7 999 1234567", "+79991234567"),
        ("9991234567", "+79991234567"),
        ("+1 234 567 8900", "+12345678900"),  # другой код страны
        ("(999) 123-45-67", "+79991234567"),
        ("тел: 8-999-123-45-67", "+79991234567"),
    ]

    for phone, expected in test_phones:
        result = normalize_phone(phone)
        status = "✓" if result == expected else "✗"
        print(f"{status} {phone:25} -> {result:15} (expected: {expected})")