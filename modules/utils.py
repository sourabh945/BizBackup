import subprocess 
import os
import threading
import queue
import multiprocessing as mp
import json
import asyncio
from datetime import datetime as dt

### modules imports #######################

from modules.error import error

from modules.__scripts__ import Paths

""" section for run commands """


### this function is for launch the sub process 

def run_cmd(command,input:str=None,shell:bool=False,capture_output:bool=True) -> subprocess.CompletedProcess:
    if type(command) == type(str()):
        cmd = [x for x in command.split(' ') if x != ' ' and x != ""]
    elif type(command) == type(list()):
        cmd = command
    try:
        if input:
            return subprocess.run(cmd,input=input,capture_output=capture_output,text=True,shell=shell)
        else:
            return subprocess.run(cmd,capture_output=capture_output,text=True,shell=shell) 
    except Exception as err:
        error('Unable to run the cmd please see the output below for debug.')
        print(f'\n[Output] {err}')
        
### this function initiate the program in as main process
        
def initiate_cmd(command:str):
    return os.system(command)


"""-----------------------------------------------------------------------------------------------------------------------------------"""

def script_finder(program:str) -> str:

    shell = os.getenv('SHELL')
    if shell and 'bash' in shell:
        return Paths[f'{program}_bash']
    elif 'pwsh' in os.getenv('_'):
        return Paths[f'{program}_ps']
    elif os.getenv('ComSpec') and 'cmd' in os.getenv('ComSpec'):
        return Paths[f'{program}_cmd']
    else:
        error('The terminal shell is neither bash, PowerShell, nor cmd.')


"""-----------------------------------------------------------------------------------------------------------------------------------"""



""" section for rlcone commands """



### this check the rclone is present or not in the computer
                   
def rclone_exists():
    return True if run_cmd('rclone version').returncode == 0 else False

### this function give all the list of the available drives in the rclone

def remote_list():
    return [remote for remote in (run_cmd('rclone listremotes').stdout).split('\n') if remote != ""]

### this function is called to generate new remote using rclone

def generate_remote():
    if rclone_exists():
        print("Please follow the following instruction to make the rclone drive")
        print("\n"+'-'*15+'\n')
        if not initiate_cmd('rclone config'):
            print('\n Successful to create remote')
        else:
            error('unable to create new remote')
    else:
        error('Rclone is not installed. Please install it. Use "winget install rclone" in windows and "sudo apt/dnf/pacman install rclone" in linux distros')


def get_folders(remote_path:str) -> list:
    output = run_cmd(f'rclone lsd {remote_path}')
    if output.returncode != 0 :
        error(output.stderr)
    return [ (i.split('-1')[-1]).lstrip() for i in (output.stdout).split('\n') if i != ""]

def approcach_remote(remote_path:str) -> bool:
    output = (run_cmd(f'rclone lsd {remote_path}'))
    value = output.returncode
    if value == 0 :
        return True
    elif value == 3:
        return False
    else:
        error(output.stderr)

"""-----------------------------------------------------------------------------------------------------------------------------------"""


""" section for file operations """


### this function index the given path and return into json 

def _indexer(path:str,output_queue:queue) -> None:
    output = subprocess.run(['rclone','lsjson','-R',path],capture_output=True,text=True)
    output_queue.put((path,output))

### this function uses multithreading to get the indexing from _indexder funcion 

def indexer(source_path:str,drive_path:str) -> list[list[dir]]:
    """return source_list,drive_list"""
    output = queue.Queue()

    source_thread = threading.Thread(target=_indexer,args=(source_path,output))
    drive_thread = threading.Thread(target=_indexer,args=(drive_path,output))

    drive_thread.start() 
    source_thread.start()

    drive_thread.join()
    source_thread.join()

    if (output.empty()):
        error('Internal error : The Multithreading is not working')
    while not output.empty():
        name, data = output.get()
        if name == source_path:
            source_data = data 
        else:
            drive_data = data
    
    if source_data.returncode == 0 :
        source_list = json.loads(source_data.stdout)
    else:
        error(source_data.stderr)

    if drive_data.returncode == 0 :
        drive_list = json.loads(drive_data.stdout)
    else:
        error(drive_data.stderr)

    return source_list,drive_list




"""-----------------------------------------------------------------------------------------------------------------------------------"""



""" section for backup commands"""


### this function is use for upload the files to remote

def upload_file(file_path:str,path_in_remote:str) -> bool:
    print(f'[ Uploading ] {file_path} --> {path_in_remote}')
    value = True if (run_cmd(['rclone','copyto',file_path,path_in_remote,'--ignore-checksum', '--ignore-size', '--ignore-times', '--immutable', '--metadata', '--no-check-dest'],capture_output=False)).returncode == 0 else False
    if value == True:
        print(f'[ Done ] {file_path}')
    else:
        print(f'[ Fail ] {file_path} ')
    return value 

### this function is for download the file from the remote

def download_file(file_path:str,path_in_remote:str,ouput_file:str,logs_file:str='./logs/logs.txt',fails_file:str='./logs/fails.txt') -> bool:
    print(f'[ Downloading ] {path_in_remote} --> {file_path}')
    value =  True if (run_cmd(['rclone','copyto',path_in_remote,file_path,'--ignore-checksum', '--ignore-size', '--ignore-times', '--immutable', '--metadata', '--no-check-dest'],capture_output=False)).returncode == 0 else False
    if value == True:
        print(f'[ Done ] {path_in_remote} ')
        os.system(f"'{ouput_file}' '{file_path}' '{path_in_remote}' 0 '{logs_file}' '{fails_file}'")
    else:
        print(f'[ Fail ] {path_in_remote}')
        os.system(f"'{ouput_file}' '{file_path}' '{path_in_remote}' 0 '{logs_file}' '{fails_file}'")
    return value

### this function is for sync all the files to the remote 

def sync_remote(backup_folder_path:str,remote_backup_folder_path:str) -> bool:
    """note: that this function make a copy of the current backup folder content but it delete all the old file in the remote"""
    output = (run_cmd(['rclone','sync',backup_folder_path,remote_backup_folder_path,'--progress'],capture_output=False))
    value = True if output.returncode == 0 else False
    if value == False:
        print(output.stderr)
    return value

### this function is for sync the drive from the remote. It is use when we need to setup a new backup folder copy to computer

def sync_local(backup_folder_path:str,remote_backup_folder_path:str) -> bool:
    """note: that this function make a copy of the current backup folder content but it delete all the old file in the remote"""
    output = (run_cmd(['rclone','sync',remote_backup_folder_path,backup_folder_path,'--progress'],capture_output=False))
    value = True if output.returncode == 0 else False
    os.system(f'')
    if value == False:
        print(output.stderr)
    return value

"""-----------------------------------------------------------------------------------------------------------------------------------"""

def _runner(func,file:dict,local_base:str,remote_base:str,ouput_file:str,logs_file:str='./logs/logs.txt',fails_file:str='./logs/fails.txt') -> None:
    if file.get('Drive_Path'):
        drive_path = remote_base+file['Drive_path']
    else:
        drive_path = remote_base+file['Path']
    file_path = local_base+file['Path']
    return func(file_path=file_path,path_in_remote=drive_path,ouput_file=ouput_file,logs_file=logs_file,fails_file=fails_file)
    

"""-----------------------------------------------------------------------------------------------------------------------------------"""


""" section for run backup command using multiprocessing """

def runner(func,file_list:list[dict],local_base:str,remote_base:str,ouput_file:str,logs_file:str='./logs/logs.txt',fails_file:str='./logs/fails.txt') -> list:
    print("\n Process is started...")
    os.system(f'echo "------------------------------------------------------------------" >> "{logs_file}"; echo "Date : {dt.now()}" >> "{logs_file}"; echo "" >> "{logs_file}"')
    fails = []
    with mp.Pool(processes=2*mp.cpu_count()+1) as pool:
        for file in file_list:
            result = pool.apply_async(_runner,args=(func,file,local_base,remote_base,ouput_file,logs_file,fails_file))
            if not result:
                fails.append(file)
        pool.close()
        pool.join()
    return fails

""" section for upload files function using asyncio for the uploads with 2 seconds wait """

async def _uploader(file_path:str,path_in_remote:str,output_file:str,sleep_time:float=2,logs_path:str='./logs/logs.txt',fails_path:str='./logs/fails.txt') -> asyncio.coroutines:
    print(f'\n[ Uploading ] {file_path} --> {path_in_remote}')
    process = await asyncio.create_subprocess_shell(f'rclone copyto "{file_path}" "{path_in_remote}" --ignore-checksum --ignore-size --ignore-times --immutable --metadata --no-check-dest ; code=$(echo $?) ; "{output_file}" "{file_path}" "{path_in_remote}"  $code "{logs_path}" "{fails_path}"')
    await asyncio.sleep(sleep_time)
    return process


async def uploader(file_list:list[dict],local_base:str,remote_base:str,output_file:str,sleep_time:float=2,logs_file:str='./logs/logs.txt',fails_file:str='./logs/fails.txt') -> list[str]:
    print(f'[ Start ] Uploading... ')
    tasks = []
    os.system(f'echo "------------------------------------------------------------------" >> "{logs_file}"; echo "Date : {dt.now()}" >> "{logs_file}"; echo "" >> "{logs_file}"')
    for file in file_list:
        if file.get('Drive_Path'):
            drive_path = remote_base+file['Drive_Path']
        else:
            drive_path = remote_base+file['Path']
        file_path = local_base + file['Path']
        tasks.append(await _uploader(file_path,drive_path,output_file,sleep_time,logs_file,fails_file))
    for task in tasks:
        await task.wait()
    try:
        with open(fails_file) as file:
            return file.readlines()
    except:
        return []