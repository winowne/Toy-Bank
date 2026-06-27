import json
from src.generator import gen_hello, gen_goodbye
from src.main_menu import main_menu
import os
import getpass

with open('data/data.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

GREEN = '\033[38;2;0;204;68m'
RESET = '\033[0m'
BOLD = '\033[1m'
DIM = '\033[2m'
BLINK = '\033[5m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
RED = '\033[31m'


def main():
    os.system('clear')
    print(f'''{PURPLE}{BOLD}┌─────────────────────────────────────────────────────────────────────────┐{RESET}

{GREEN}  ██████╗  █████╗ ███╗   ██╗██╗  ██╗ ██████╗ ███╗   ███╗ █████╗ ████████╗
  ██╔══██╗██╔══██╗████╗  ██║██║ ██╔╝██╔═══██╗████╗ ████║██╔══██╗╚══██╔══╝
  ██████╔╝███████║██╔██╗ ██║█████╔╝ ██║   ██║██╔████╔██║███████║   ██║   
  ██╔══██╗██╔══██║██║╚██╗██║██╔═██╗ ██║   ██║██║╚██╔╝██║██╔══██║   ██║   
  ██████╔╝██║  ██║██║ ╚████║██║  ██╗╚██████╔╝██║ ╚═╝ ██║██║  ██║   ██║   
  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   {RESET}
{PURPLE}{BOLD}
├─────────────────────────────────────────────────────────────────────────┤{RESET}''')
    try:
        print(f'  Для выхода из системы введите {CYAN}{BOLD}0000{RESET}')
        pin = getpass.getpass(f'{CYAN}  Введите {BOLD}ПИН-код: {RESET}', echo_char=f'*')

        if pin == '0000':
            print(gen_goodbye())
            exit()

        current_user = None

        for u in config.values():
            if str(u['pin']) == pin:
                current_user = u
                break

        if current_user:
            username = current_user["username"]
            user_balance = current_user["balance"]

            hello = gen_hello()
            print(f'  {hello}{RESET}, {PURPLE}{BOLD}{username}{RESET}')
            print(f'{PURPLE}{BOLD}├─────────────────────────────────────────────────────────────────────────┤{RESET}')
            main_menu(username, user_balance)
        else:
            print(f'  {RED}{BOLD}Неверный ПИН-код{RESET}')
    except ValueError:
        print(f'  {RED}{BOLD}Ошибка:{RESET} {RED}ПИН-код должен состоять из цифр{RESET}')


if __name__ == '__main__':
    main()