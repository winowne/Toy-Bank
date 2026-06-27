import os
from src.generator import gen_goodbye
from src.transfer import transfer

GREEN = '\033[38;2;0;204;68m'
RESET = '\033[0m'
BOLD = '\033[1m'
DIM = '\033[2m'
BLINK = '\033[5m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
RED = '\033[31m'

def main_menu(username, balance):
    os.system("clear")
    print(f'''{PURPLE}{BOLD}┌─────────────────────────────────────────────────────────────────────────┐{RESET}
  Пользователь: {GREEN}{BOLD}{username}{RESET} | Баланс: {GREEN}{BOLD}{balance} руб.{RESET}
{PURPLE}{BOLD}├─────────────────────────────────────────────────────────────────────────┤{RESET}
  {PURPLE}{BOLD}[1]{RESET} Перевести деньги
  {PURPLE}{BOLD}[2]{RESET} Выйти
{PURPLE}{BOLD}├─────────────────────────────────────────────────────────────────────────┤{RESET}''')
    choice = int(input(f'{CYAN}{BLINK}->(): {RESET}'))

    if choice == 1:
        transfer(username,balance)

    elif choice == 2:
        gen_goodbye()
        exit()
