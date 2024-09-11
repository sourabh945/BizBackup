import os

### module imports

from modules.error import error
from modules.ui import select_folder , select_drive

### configuration file reader for paths 

def configurator() -> list[str,str]:

    import configparser

    config = configparser.ConfigParser()

    if 'config.ini' not in os.listdir('./'):
        error('The configuration file is not find !!!')
        print('Please enter the path details for installation')
        drive_path = select_folder()
        source_path = select_drive()
        value = input('Please name the folder in drive you wanted to store it :') 
        value = value.lstrip()
        value = value.rstrip()
        if value[-1] != "/":
            drive_path += value + "/"
        else:
            drive_path += value
        with open('config.ini','w+a') as file:
            config['folders'] = {'drive_path':drive_path,'source_path':source_path}
            config.write(file)
    else:
        config.read('./config.ini')
        source_path = config.get('folders','source_path')
        drive_path = config.get('folders','drive_path')

    return drive_path , source_path


