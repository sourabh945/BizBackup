import os

import configparser

### module imports

from modules.error import error
from modules.ui import select_folder , select_drive , select_remote_folder

from modules.f_ops import check_paths
from modules.utils import approcach_remote

from modules.__scripts__ import scripts,Paths

########################################

base = "."

###########################################


### configuration file reader for paths 

def checks(source_path:str,drive_path:str):
    print('[ Checking ] Path Checking...')
    check_paths(source_path)
    if not approcach_remote(drive_path):
        error('Unable to connect to drive')
    print('[ Complete ] Checking ')

        

def configurator() -> list[str,str]:

    config = configparser.ConfigParser()

    if 'config.ini' not in os.listdir(base+'/configurations/'):

        print('The configuration file is not find !!!')
        print('Please enter the path details for installation')

        source_path = select_folder()
        drive_path= select_drive()

        drive_path += select_remote_folder(drive_path) + "/"

        checks(source_path,drive_path)

        with open(base+'/configurations/config.ini','w') as file:
            config['folders'] = {'drive_path':drive_path,'source_path':source_path}
            config.write(file)
    else:
        config.read(base+'/configurations/config.ini')
        source_path = config.get('folders','source_path')
        drive_path = config.get('folders','drive_path')

        checks(source_path,drive_path)

    return drive_path , source_path


"""------------------------------------------------------------------------------------------------------------------------------------"""

def advance_config_loader() -> list:
    "log file path , fails path file , sleep time"

    config = configparser.ConfigParser()

    if not os.path.isdir(base+'/configurations'):
        os.mkdir(base+'/configurations')

    if 'advance.ini' not in os.listdir(base+'/configurations/'):

        with open(base+'/configurations/advance.ini','w') as file:
            config['folders'] = {'log_folder':base+'/logs','logs_file_path':base+'/logs/logs.txt','fails_file_path':base+'/logs/fails.txt'}
            config['time'] = {'sleep_time':2}
            config.write(file)

        return base+'/logs',base+'/logs/logs.txt' , base+'/logs/fails.txt' , 2

    else:
        try:
            config.read(base+'/configurations/advance.ini')
            return config.get('folders','log_folder'), config.get('folders','logs_file_path'),config.get('folders','fails_file_path'),float(config.get('time','sleep_time'))
        except Exception as err:
            error(f'{err}. Please delete the advance.ini the system was create new one.')
    

"""----------------------------------------------------------------------------------------------------------------------------------------"""

def log_maker(folder,logs,fails):
    if not os.path.isdir(folder):
        os.mkdir(folder)
        return 0
    if os.path.isfile(fails):
        os.remove(fails)

"""-------------------------------------------------------------------------------------------------------------------------------------------"""


def scripts_writer():
    if 'scripts' not in os.listdir(base+'/') : os.mkdir(base+'/scripts/')
    folder_content = os.listdir(base+'/scripts')
    for script_name in Paths.keys():
        if os.path.basename(Paths[script_name]) not in folder_content:
            file = open(Paths[script_name],'w') 
            file.write(scripts[script_name])
            file.close()
        os.system(f'chmod +x "{Paths[script_name]}"')