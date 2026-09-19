from __future__ import annotations

import getpass
import os

from src.bank import Bank, BankError
from src.generator import gen_goodbye, gen_hello

GREEN = "\033[38;2;0;204;68m"
RESET = "\033[0m"
BOLD = "\033[1m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
RED = "\033[31m"


def clear_screen() -> None:
    if os.name == "nt":
        os.system("cls")
    else:
        print("\033[2J\033[H", end="")


def header(user: dict | None = None) -> None:
    clear_screen()
    print(f"{PURPLE}{BOLD}=============================================={RESET}")
    print(f"{GREEN}{BOLD}                 BANK CONSOLE{RESET}")
    if user:
        print(f"  Пользователь: {GREEN}{user['username']}{RESET} | Баланс: {GREEN}{user['balance']} руб.{RESET}")
    print(f"{PURPLE}{BOLD}=============================================={RESET}")


def authenticate(bank: Bank) -> dict | None:
    print(f"Для выхода введите {CYAN}{BOLD}0000{RESET}")
    for attempt in range(3):
        pin = getpass.getpass(f"{CYAN}Введите PIN-код: {RESET}").strip()
        if pin == "0000":
            return None
        if pin.isdigit():
            user = bank.authenticate(pin)
            if user is not None:
                return user
        remaining = 2 - attempt
        if remaining:
            print(f"{RED}Неверный PIN-код. Осталось попыток: {remaining}{RESET}")
    print(f"{RED}Слишком много неудачных попыток. Сеанс завершен.{RESET}")
    return None


def show_history(bank: Bank, user: dict) -> None:
    operations = bank.user_history(str(user["username"]))
    if not operations:
        print("История операций пуста.")
        return
    print("\nИстория операций:")
    for operation in operations:
        kind = operation.get("type", "transfer")
        if kind == "deposit":
            description = f"пополнение +{operation['amount']} руб."
        elif kind == "withdraw":
            description = f"снятие -{operation['amount']} руб."
        else:
            direction = "->" if operation["sender"].casefold() == str(user["username"]).casefold() else "<-"
            other = operation["recipient"] if direction == "->" else operation["sender"]
            description = f"{direction} {other}: {operation['amount']} руб."
        print(f"  {operation['created_at']}  {description}")


def menu(bank: Bank, user: dict) -> None:
    while True:
        header(user)
        print("  1. Перевести деньги")
        print("  2. Пополнить баланс")
        print("  3. Снять деньги")
        print("  4. История операций")
        print("  5. Сменить PIN-код")
        print("  6. Выйти")
        choice = input(f"\n{CYAN}-> {RESET}").strip()
        if choice == "1":
            recipient = input("Фамилия получателя (или 0000 для отмены): ").strip()
            if recipient == "0000":
                continue
            amount_text = input("Сумма перевода: ").strip()
            if amount_text == "0000":
                continue
            try:
                amount = int(amount_text)
                operation = bank.transfer(user, recipient, amount)
                print(f"{GREEN}Перевод выполнен: {operation['amount']} руб.{RESET}")
            except (ValueError, TypeError):
                print(f"{RED}Сумма должна быть целым числом.{RESET}")
            except BankError as error:
                print(f"{RED}{error}{RESET}")
            input("Нажмите Enter, чтобы продолжить...")
        elif choice in {"2", "3"}:
            amount_text = input("Сумма (или 0000 для отмены): ").strip()
            if amount_text == "0000":
                continue
            try:
                amount = int(amount_text)
                operation = bank.deposit(user, amount) if choice == "2" else bank.withdraw(user, amount)
                print(f"{GREEN}Операция выполнена: {operation['amount']} руб.{RESET}")
            except (ValueError, TypeError):
                print(f"{RED}Сумма должна быть целым числом.{RESET}")
            except BankError as error:
                print(f"{RED}{error}{RESET}")
            input("Нажмите Enter, чтобы продолжить...")
        elif choice == "4":
            header(user)
            show_history(bank, user)
            input("\nНажмите Enter, чтобы продолжить...")
        elif choice == "5":
            old_pin = getpass.getpass("Текущий PIN: ").strip()
            new_pin = getpass.getpass("Новый PIN: ").strip()
            try:
                bank.change_pin(user, old_pin, new_pin)
                print(f"{GREEN}PIN-код изменен.{RESET}")
            except BankError as error:
                print(f"{RED}{error}{RESET}")
            input("Нажмите Enter, чтобы продолжить...")
        elif choice == "6":
            print(gen_goodbye())
            return
        else:
            print(f"{RED}Неверный пункт меню.{RESET}")


def main() -> None:
    try:
        bank = Bank()
        header()
        user = authenticate(bank)
        if user is not None:
            print(f"{gen_hello()}, {user['username']}!")
            menu(bank, user)
        else:
            print(gen_goodbye())
    except (EOFError, KeyboardInterrupt):
        print("\nСеанс завершен.")
    except ValueError as error:
        print(f"{RED}Ошибка данных: {error}{RESET}")


if __name__ == "__main__":
    main()
