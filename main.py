import json
from src.generator import gen_hello
import os
import getpass

with open('data/data.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

GREEN = '\033[38;2;0;204;68m'
RESET = '\033[0m'
BOLD = '\033[1m'
DIM = '\033[2m'
BLINK = '\033[5m'

def main():
    os.system('clear')
    print(f'''{GREEN}
██████╗  █████╗ ███╗   ██╗██╗  ██╗ ██████╗ ███╗   ███╗ █████╗ ████████╗
██╔══██╗██╔══██╗████╗  ██║██║ ██╔╝██╔═══██╗████╗ ████║██╔══██╗╚══██╔══╝
██████╔╝███████║██╔██╗ ██║█████╔╝ ██║   ██║██╔████╔██║███████║   ██║   
██╔══██╗██╔══██║██║╚██╗██║██╔═██╗ ██║   ██║██║╚██╔╝██║██╔══██║   ██║   
██████╔╝██║  ██║██║ ╚████║██║  ██╗╚██████╔╝██║ ╚═╝ ██║██║  ██║   ██║   
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   
{RESET}''')

    try:
        pin = getpass.getpass(f'Введите {BOLD}ПИН-код: {RESET}', echo_char='*')
        current_user = None
        for u in config.values():
            if str(u['pin']) == pin:
                current_user = u
                break

        if current_user:
            username = current_user["username"]
            hello = gen_hello()
            print(f'{hello}{RESET},{GREEN}{BOLD}{username}{RESET}')
        else:
            print('Неверный ПИН-код')
    except ValueError:
        print('Ошибка: ПИН-код должен состоять из цифр')

if __name__ == '__main__':
    main()