import os

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

    import configparser

    config = configparser.ConfigParser()

    if 'config.ini' not in os.listdir('./'):

        print('The configuration file is not find !!!')
        print('Please enter the path details for installation')

        source_path = select_folder()
        drive_path= select_drive()

        drive_path += select_remote_folder(drive_path) + "/"

        checks(source_path,drive_path)

        with open('config.ini','w') as file:
            config['folders'] = {'drive_path':drive_path,'source_path':source_path}
            config.write(file)
    else:
        config.read('./config.ini')
        source_path = config.get('folders','source_path')
        drive_path = config.get('folders','drive_path')

        checks(source_path,drive_path)

    return drive_path , source_path


