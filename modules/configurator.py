import os

import configparser

### module imports

from modules.error import error
from modules.ui import select_folder , select_drive , select_remote_folder

from modules.f_ops import check_paths
from modules.utils import approcach_remote

### configuration file reader for paths 

def checks(source_path:str,drive_path:str):
    print('[ Checking ] Path Checking...')
    check_paths(source_path)
    if not approcach_remote(drive_path):
        error('Unable to connect to drive')
    print('[ Complete ] Checking ')

        

def configurator() -> list[str,str]:

    config = configparser.ConfigParser()

    if 'config.ini' not in os.listdir('./configurations/'):

        print('The configuration file is not find !!!')
        print('Please enter the path details for installation')

        source_path = select_folder()
        drive_path= select_drive()

        drive_path += select_remote_folder(drive_path) + "/"

        checks(source_path,drive_path)

        with open('./configurations/config.ini','w') as file:
            config['folders'] = {'drive_path':drive_path,'source_path':source_path}
            config.write(file)
    else:
        config.read('./configurations/config.ini')
        source_path = config.get('folders','source_path')
        drive_path = config.get('folders','drive_path')

        checks(source_path,drive_path)

    return drive_path , source_path


"""------------------------------------------------------------------------------------------------------------------------------------"""

def advance_config_loader() -> list:
    "log file path , fails path file , sleep time"

    config = configparser.ConfigParser()

    if 'advance.ini' not in os.listdir('./configurations/'):

        with open('./configurations/advance.ini','w') as file:
            config['folders'] = {'logs_file_path':'./logs/logs.txt','fails_file_path':'./logs/fails.txt'}
            config['time'] = {'sleep_time':2}
            config.write(file)

        return './logs.txt' , './fails.txt' , 2

    else:
        config.read('./configurations/advance.ini')
        return config.get('folders','logs_file_path'),config.get('folders','fails_file_path'),float(config.get('time','sleep_time'))