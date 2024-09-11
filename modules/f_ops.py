import os 

### modules imports #####################

from modules.error import error

### this func is for find the path is exist or not

def check_paths(path:str) -> None:
    if os.path.isdir(path) is False:
        error(f'Path {path} is not found !!! ')
        
        
### this function use for rename the name of the modifiled files before upload to drive which have its own version on drive 
### and this function the return the dict which have additional two key values drive_path and drive_name

def get_new_name(item:dict) -> dict:
    additional_string = f"_({(item['ModTime'])[0:list(item['ModTime']).index('.')]})"
    drive_path = item['Path'][0:list(item['Path']).index('.')]+additional_string+item['Path'][list(item['Path']).index('.'):]
    drive_name = item['Name'][0:list(item['Name']).index('.')]+additional_string+item['Name'][list(item['Name']).index('.'):]
    item['Drive_Path'] = drive_path
    item['Drive_Name'] = drive_name
    return item


### this function do all the sorting for us

def get_sorted(source_list:list[dict],drive_list:list[dict]) -> list[list[dict]]:
    """It return  uploads_list , download_list ,  upload_size , download_size , number of modified files"""
    
    download_list = [] 

    upload_size , download_size , new_folders , modified_files = 0 , 0 , 0 , 0

    drive_set = set() 
    upload_dict = {}

    for item in drive_list:
        drive_set.add((item["Path"],item["Name"],item["Size"],item["ModTime"].split(".")[0],item["IsDir"]))

    while source_list != [] : 
        item = source_list.pop(0)
        if item['IsDir'] is not True:
            time = (item['ModTime']).split(".")[0] 
            if (item["Path"],item["Name"],item["Size"],time,item["IsDir"]) in drive_set:
                drive_set.remove((item["Path"],item["Name"],item["Size"],time,item["IsDir"]))
            else:
                upload_dict[item['Path']] = item 
                upload_size += item['Size']

    for item in drive_set:
        if item[4] is False:
            if item[0] in upload_dict.keys():
                upload_dict[item[0]] = get_new_name(upload_dict[item[0]])
                modified_files += 1
            else:
                download_list.append({"Path": item[0],"Name": item[1],"Size": item[2],"ModTime": item[3],"IsDir": item[4]})
                download_size += item[2]
    
    return list(upload_dict.values()) , download_list , upload_size , download_size , modified_files


################ is empty ######################################################################################

def is_empty(list:list[dict]):
    for item in list:
        if item['IsDir'] is False:
            return False
    return True