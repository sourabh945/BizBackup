from colorama import Fore

### error startement

def error(message:str) -> None:
    print(Fore.RED+'[ERROR] '+Fore.WHITE+message)
    print('\n If you unable to solve the issue. Please report on https://github.com/sourabh945/BizBackup.git/issues \n')
    exit(1)