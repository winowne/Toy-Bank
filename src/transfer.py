import os
import json
import time

with open('data/data.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

all_users = [u["username"].lower() for u in config.values()]

GREEN = '\033[38;2;0;204;68m'
RESET = '\033[0m'
BOLD = '\033[1m'
DIM = '\033[2m'
BLINK = '\033[5m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
RED = '\033[31m'


def transfer(username, balance):
    os.system('clear')
    print(f'''{PURPLE}{BOLD}┌─────────────────────────────────────────────────────────────────────────┐{RESET}
  Пользователь: {GREEN}{BOLD}{username}{RESET} | Баланс: {GREEN}{BOLD}{balance} руб.{RESET}
{PURPLE}{BOLD}├─────────────────────────────────────────────────────────────────────────┤{RESET}''')

    recipient = input(f'  {CYAN}Укажите {BOLD}фамилию{RESET} {CYAN}получателя: {RESET}').strip().lower()
    time.sleep(1)
    print('\033[F\033[K', end='')

    if not recipient.isalpha():
        print(f'  {RED}{BOLD}Ошибка:{RESET} {RED}{BOLD}Фамилия{RESET} {RED}должна состоять из букв{RESET}')
    else:
        if recipient in all_users:
            print(f'  Получатель: {GREEN}{BOLD}{recipient}{RESET}')
            time.sleep(1)
            print('\033[F\033[K', end='')

            try:
                print(f'  Для выхода из системы введите {CYAN}{BOLD}0000{RESET}')
                amount_input = input(f"  {CYAN}Введите {BOLD}сумму{RESET} {CYAN}перевода: {RESET}").strip()

                if amount_input == '0000':
                    print("  Перевод отменен.")
                    time.sleep(2)
                    return

                amount = int(amount_input)

                if 0 < amount <= balance:
                    for u in config.values():
                        if u["username"].lower() == username.lower():
                            u["balance"] -= amount
                            balance = u["balance"]
                            break

                    for u in config.values():
                        if u["username"].lower() == recipient:
                            u["balance"] += amount
                            break

                    with open("data/data.json", "w", encoding="utf-8") as file:
                        json.dump(config, file, indent=4, ensure_ascii=False)

                    try:
                        with open("data/transfers.json", "r", encoding="utf-8") as f:
                            transfers_history = json.load(f)
                    except (FileNotFoundError, json.JSONDecodeError):
                        transfers_history = []

                    new_transfer = {
                        "username": username,
                        "transfer": amount,
                        "whom": recipient
                    }
                    transfers_history.append(new_transfer)

                    with open("data/transfers.json", "w", encoding="utf-8") as file:
                        json.dump(transfers_history, file, indent=4, ensure_ascii=False)

                    print(f'  Успешно переведено {GREEN}{BOLD}{amount}{RESET} руб. получателю {GREEN}{BOLD}{recipient}{RESET}')
                    time.sleep(2)
                    from src.main_menu import main_menu
                    main_menu(username, balance)
                else:
                    print(f'  {RED}{BOLD}Ошибка:{RESET} Недостаточно средств или неверная сумма!')
                    from src.main_menu import main_menu
                    main_menu(username, balance)

            except ValueError:
                print(f'  {RED}{BOLD}Ошибка:{RESET} {RED}сумма перевода должна состоять из цифр{RESET}')
        else:
            print(f'  {RED}{BOLD}Ошибка:{RESET} Такого {RED}{BOLD}пользователя{RESET} {RED}не существует{RESET}')