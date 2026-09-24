import os
import random
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from shared.student import STUDENT_NAME, VARIANT_NUMBER


def main():
    passwords = [
        "UserPass1!",
        "temp",
        "Cyber$ecur1ty",
        "guest",
        "P0w3rful@Pass",
        "login",
        "Defens3#2023",
        "abc123",
        "Elit3@Secur",
        "demo",
    ]
    criteria = {
        "min_length": 9,
        "require_digits": True,
        "require_upper": True,
        "require_special": True,
    }
    forbidden_passwords = {"temp", "guest", "login", "demo", "abc123", "user"}

    for _ in range(3):
        random_index = random.randint(0, len(passwords) - 1)
        passwords.append(passwords[random_index])

    print(f"\n{STUDENT_NAME} (Варіант {VARIANT_NUMBER})")
    print("Аналіз паролів")
    print(f"{'Пароль':<20} | {'Статус':<15}")
    print("-" * 38)

    for pwd in passwords:
        has_digit = any(char.isdigit() for char in pwd)
        has_upper = any(char.isupper() for char in pwd)
        has_lower = any(char.islower() for char in pwd)
        has_special = any(not char.isalnum() for char in pwd)

        criteria_met_count = sum([has_digit, has_upper, has_lower, has_special])
        all_criteria_met = has_digit and has_upper and has_lower and has_special

        if pwd in forbidden_passwords or len(pwd) < criteria["min_length"]:
            status = "Заборонений"
        elif all_criteria_met:
            if len(pwd) >= criteria["min_length"] + 4 and passwords.count(pwd) == 1:
                status = "Дуже сильний"
            else:
                status = "Сильний"
        elif criteria_met_count > 1:
            status = "Середній"
        elif criteria_met_count >= 1:
            status = "Слабкий"

        print(f"{pwd:<20} | {status:<15}")


if __name__ == "__main__":
    main()
