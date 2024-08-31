import os
from colorama import Fore

### module imports

from modules.file_operation import error

### configuration file reader for paths 

def configurator() -> list[str,str]:

    import configparser

    config = configparser.ConfigParser()

    if 'config.ini' not in os.listdir('./'):
        error('The configuration file is not find !!!')
        print(Fore.WHITE+'Please enter the path details for installation')
        drive_path = input("Enter the path of the rclone drive with folder path: ")
        source_path = input("Enter the source director path : ")
        with open('config.ini','w+a') as file:
            config['folders'] = {'drive_path':drive_path,'source_path':source_path}
            config.write(file)
    else:
        config.read('./config.ini')
        source_path = config.get('folders','source_path')
        drive_path = config.get('folders','drive_path')

    return drive_path , source_path
