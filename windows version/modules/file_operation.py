import os 
import subprocess
import threading

from colorama import Fore

### error startement

def error(message:str) -> None:
    print(Fore.RED+'[ERROR] '+Fore.WHITE+message)
    print('\n If you unable to solve the issue. Please report on https://github.com/sourabh945/BizBackup.git/issues \n')
    exit(1)


### this func is for find the path is exist or not

def check_paths(path:str) -> None:
    if os.path.isdir(path) is False:
        print('\n'+Fore.RED+'[ERROR] '+Fore.WHITE+'[{path}] is not found in filesystem')
        exit(1)

### this function index the given path and return into json 

def _indexer(path:str,output_queue:queue) -> None:
    output = subprocess.run(['rlcone','lsjson','-R',path],capture_output=True,text=True)
    output_queue.put((path,output))

### this function uses multithreading to get the indexing from _indexder funcion 

def indexer(source_path:str,drive_path:str) -> list[list[dir]]:

    check_paths(source_path)
    check_paths(drive_path)

    output = queue.Queue()

    source_thread = threading.Thread(target=_indexer,args=(source_path,output))
    drive_thread = threading.Thread(target=_indexer,args=(drive_path,output))

    drive_thread.start() 
    source_thread.start()

    drive_thread.join()
    source_thread.join()

    if (output.empty()):
        error('Internal error. please report on https://github.com/sourabh945/BizBackup.git/issues : The Multithreading is not working')
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

### this function make folder in the drive and local system

def make_dirs(path:str,list:list) -> list[dict]:
    return_list = []
    for dir in list:
        if dir['IsDir'] is True:
            os.mkdir(path+dir['Path'])
        else:
            return_list.append(dir)
    return return_list

### this function use for rename the name of the modifiled files before upload to drive which have its own version on drive 
### and this function the return the dict which have additional two key values drive_path and drive_name

def get_new_name(item:dict) -> dict:
    additional_string = f'_({item['ModTime'][0:list(item['ModTime']).index('.',-1)]})'
    drive_path = item['Path'][0:list(item['Path']).index('.',-1)]+additional_string+item['Path'][list(item['Path']).index('.',-1):]
    drive_name = item['Name'][0:list(item['Name']).index('.',-1)]+additional_string+item['Name'][list(item['Name']).index('.',-1):]
    item['Drive_Path'] = drive_path
    item['Drive_Name'] = drive_name
    return item


### this function do all the sorting for us

def get_sorted(source_list:list[dict],drive_list:list[dict]) -> list[list[dict]]:
    
    download_list , new_dirs_list  = [] , [] 

    upload_size , download_size , new_folders , modified_files = 0 , 0 , 0 , 0

    drive_set = set() 
    upload_dict = {}

    for i in drive_list:
        drive_set.add((item["Path"],item["Name"],item["Size"],item["ModTime"],item["IsDir"]))

    while source_list != [] : 
        item = source_list.pop(0)
        if item['IsDir'] is not True:
            if (item["Path"],item["Name"],item["Size"],item["ModTime"],item["IsDir"]) in drive_set:
                drive_set.remove((item["Path"],item["Name"],item["Size"],item["ModTime"],item["IsDir"]))
            else:
                upload_dict[item['Path']] = item 
                upload_size += item['Size']

    for item in drive_set:
        if item[4] is True:
            new_dirs_list.append({"Path": item[0],"Name": item[1],"Size": item[2],"ModTime": item[3],"IsDir": item[4]})
            new_folders += 1
        else:
            if item[0] in upload_dict:
                upload_dict[item[0]] = get_new_name(upload_dict[item[0]])
                modified_files += 1
            else:
                download_list.append({"Path": item[0],"Name": item[1],"Size": item[2],"ModTime": item[3],"IsDir": item[4]})
                download_size += item[2]