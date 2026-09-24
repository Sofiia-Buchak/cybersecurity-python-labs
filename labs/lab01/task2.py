import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from shared.student import STUDENT_NAME, VARIANT_NUMBER


def main():
    users = {
        "security_chief": {
            "role": "security_officer",
            "clearance": 4,
            "department": "Security",
            "active": True,
        },
        "network_admin": {
            "role": "network_admin",
            "clearance": 3,
            "department": "Network",
            "active": True,
        },
        "help_desk": {
            "role": "support",
            "clearance": 1,
            "department": "Support",
            "active": True,
        },
        "auditor_ext": {
            "role": "auditor",
            "clearance": 3,
            "department": "Audit",
            "active": True,
        },
        "temp_worker": {
            "role": "temporary",
            "clearance": 1,
            "department": "Temp",
            "active": False,
        },
    }

    resources = [
        ("incident_reports", 4),
        ("network_topology", 3),
        ("user_manual", 1),
        ("vulnerability_scans", 3),
        ("root_access", 4),
        ("help_tickets", 1),
        ("penetration_tests", 4),
        ("firewall_rules", 3),
        ("software_licenses", 2),
        ("faq_docs", 1),
    ]

    security_levels = ("Unrestricted", "Limited", "Sensitive", "Classified")
    blocked_users = {"temp_worker", "fired_employee", "compromised_acc"}

    print(f"\n{STUDENT_NAME} (Варіант {VARIANT_NUMBER})")
    print(" " * 14 + "Система доступу")

    print(f"{'Ресурс системи':<25} | {'Рівень безпеки':<15}")
    for res_name, res_level in resources:
        level_name = security_levels[res_level - 1]
        print(f"{res_name:<25} | {level_name:<15}")

    print("\n" + " " * 24 + "Журнал перевірки доступу ")

    all_users_to_check = set(users.keys()).union(blocked_users).union({"unknown_user"})

    for username in sorted(all_users_to_check):
        for res_name, res_level in resources:
            if username not in users:
                status = "DENY (User not found)"
            elif username in blocked_users:
                status = "DENY (User is blocked)"
            elif users[username]["active"] == False:
                status = "DENY (Account inactive)"
            elif users[username]["clearance"] >= res_level:
                status = "ALLOW"
            else:
                status = "DENY (Insufficient clearance)"

            print(f"user={username:<18} resource={res_name:<20} -> {status}")


if __name__ == "__main__":
    main()
