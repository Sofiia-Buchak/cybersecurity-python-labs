import csv
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from shared.student import STUDENT_NAME, VARIANT_NUMBER

print(f"\n{STUDENT_NAME} (Варіант {VARIANT_NUMBER})")

class ValidationError(Exception):
    pass

PERSONAL_SALT = str(VARIANT_NUMBER).zfill(5)
MIN_PASSWORD_LENGTH = 8 

def generate_hash(password: str, salt: str = "00000") -> str:
    """Генерує sha1 хеш пароля із сіллю."""
    if not password or not salt:
        raise ValueError("Пароль або сіль не можуть бути порожніми.")
    
    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValidationError(f"Пароль закороткий. Мінімум {MIN_PASSWORD_LENGTH} символів.")
    
    return hashlib.sha1((password + salt).encode('utf-8')).hexdigest()

def log_event(func):
    """Декоратор для логування подій авторизації у JSON."""
    def wrapper(username, password):
        result_status = "failure"
        try:
            res = func(username, password)
            if res:
                result_status = "success"
            return res
        finally:
            log_entry = {
                "event": "login",
                "user": username,
                "result": result_status,
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                "args": [],
                "kwargs": {}
            }
            log_file_path = os.path.join(os.path.dirname(__file__), 'data', 'log.json')
            
            logs = []
            if os.path.exists(log_file_path):
                with open(log_file_path, 'r', encoding='utf-8') as f:
                    try:
                        logs = json.load(f)
                    except json.JSONDecodeError:
                        pass
            
            logs.append(log_entry)
            
            with open(log_file_path, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=4, ensure_ascii=False)
    return wrapper

def create_user(username, password):
    """Створює запис користувача з хешованим паролем."""
    hash_value = generate_hash(password, PERSONAL_SALT)
    return (username, hash_value)

def create_users(users_list):
    """Створює базу даних у CSV файлі."""
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    csv_file_path = os.path.join(data_dir, 'users.csv')
    print("Реєстрація")
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['логін', 'хеш_пароля'])
        for u, p in users_list:
            try:
                writer.writerow(create_user(u, p))
            except ValidationError as e:
                print(f"Відхилено реєстрацію користувача {u}: {e}")
            except ValueError as e:
                print(f"Відхилено реєстрацію користувача {u}: {e}")

def read_db():
    """Зчитує користувачів з CSV."""
    users_db = []
    csv_file_path = os.path.join(os.path.dirname(__file__), 'data', 'users.csv')
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader) 
        for row in reader:
            if row:
                users_db.append(row)
    return users_db

@log_event
def login(username: str, password: str) -> bool:
    """Автентифікація користувача."""
    if not username or not password:
        raise ValueError("Логін або пароль не можуть бути порожніми.")
    
    users_db = read_db()
    expected_hash = generate_hash(password, PERSONAL_SALT)
    
    for db_user, db_hash in users_db:
        if db_user == username and db_hash == expected_hash:
            return True
    return False

def main():
    print(f"{'':<20}База та Логування")
    
    users_to_register = (
        ("admin", "SuperSecure123"),
        ("user1", "Password_01"),
        ("user2", "qwertyuiop"),
        ("guest", "123"),
        ("sofia", "MyPassw0rd!"),
        ("hacker", "123456789"),
        ("manager", "Manager2023"),
        ("analyst", "An@lystPass"),
        ("tester", "Test1ngPass"),
        ("dev", "Developer##")
    )
    
    try:
        create_users(users_to_register)
        
        db = read_db()
        print(f"\n{'-'*60}")
        print(f"{'Логін':<15} | {'Хеш пароля (sha1 + сіль)'}")
        print(f"{'-'*60}")
        for user, hsh in db:
            print(f"{user:<15} | {hsh[:32]}...")
            
        print("\n--- Тестування автентифікації ---")
        print(f"Вхід admin (правильно): {'Успіх' if login('admin', 'SuperSecure123') else 'Відмова'}")
        print(f"Вхід user1 (неправильно): {'Успіх' if login('user1', 'WrongPass') else 'Відмова'}")
        
    except FileNotFoundError as e:
        print(f"Помилка: Файл не знайдено - {e}")
    except PermissionError as e:
        print(f"Помилка: Немає прав доступу - {e}")
    except OSError as e:
        print(f"Помилка вводу/виводу - {e}")
    except ValueError as e:
        print(f"Помилка значення: {e}")

if __name__ == "__main__":
    main()