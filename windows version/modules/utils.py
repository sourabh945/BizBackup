import subprocess 
import os
import threading
import queue

from modules.error import error

### this function is for launch the sub process 

def run_cmd(command:str,input:str=None,shell:bool=False) -> subprocess.CompletedProcess:
    cmd = [x for x in command.split(' ') if x != ' ' and x != ""]
    try:
        if input:
            return subprocess.run(cmd,input=input,capture_output=True,text=True,shell=shell)
        else:
            return subprocess.run(cmd,capture_output=True,text=True,shell=shell) 
    except Exception as err:
        error('Unable to run the cmd please see the output below for debug.')
        print(f'\n[Output] {err}')
        
### this function initiate the program in as main process
        
def initiate_cmd(command:str):
    return os.system(command)

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

### this function is use for upload the files to remote

def upload_file(file_path:str,path_in_remote:str) -> bool:
    return True if (run_cmd(f'rclone copyto {file_path} {path_in_remote} --ignore-checksum --ignore-size --ignore-times --immutable --metadata --no-check-dest')).returncode == 0 else False

### this function is for download the file from the remote

def download_file(file_path:str,path_in_remote:str) -> bool:
    return True if (run_cmd(f'rclone copyto {path_in_remote} {file_path} --ignore-checksum --ignore-size --ignore-times --immutable --metadata --no-check-dest')).returncode == 0 else False

### thsi function is for sync all the files to the remote 

def sync_remote(backup_folder_path:str,remote_backup_folder_path:str) -> bool:
    """note: that this function make a copy of the current backup folder content but it delete all the old file in the remote"""
    return True if (run_cmd(f'rclone sync {backup_folder_path} {remote_backup_folder_path}')).returncode == 0 else False

### this function is for sync the drive from the remote. It is use when we need to setup a new backup folder copy to computer

def sync_local(backup_folder_path:str,remote_backup_folder_path:str) -> bool:
    """note: that this function make a copy of the current backup folder content but it delete all the old file in the remote"""
    return True if (run_cmd(f'rclone sync  {remote_backup_folder_path} {backup_folder_path}')).returncode == 0 else False

### this function index the given path and return into json 

def _indexer(path:str,output_queue:queue) -> None:
    output = subprocess.run(['rlcone','lsjson','-R',path],capture_output=True,text=True)
    output_queue.put((path,output))

### this function uses multithreading to get the indexing from _indexder funcion 

def indexer(source_path:str,drive_path:str) -> list[list[dir]]:

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
        source_list = source_data.stdout
    else:
        error(source_data.stderr)

    if drive_data.returncode == 0 :
        drive_list = drive_data.stdout
    else:
        error(drive_data.stderr)

    return source_list,drive_list

def 

if __name__ == "__main__":
    print(run_cmd('rclone listremotes'))