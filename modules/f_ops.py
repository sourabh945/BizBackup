import os 

################################################ time function ###

from datetime import datetime, timezone, timedelta

def convert_to_utc(time_str):


    truncated_time_str = time_str[:26] + time_str[29:]  # Remove last three digits of fractional seconds part

    # Parse the input string with its timezone info
    dta = datetime.strptime(truncated_time_str, "%Y-%m-%dT%H:%M:%S.%f%z")
    
    # Convert to UTC
    dt_utc = dta.astimezone(timezone.utc)
    
    # Format to the required output
    return dt_utc.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'

### modules imports #####################

from modules.error import error

### this func is for find the path is exist or not

def check_paths(path:str) -> None:
    if os.path.isdir(path) is False:
        error(f'Path {path} is not found !!! ')
        
        
### this function use for rename the name of the modifiled files before upload to drive which have its own version on drive 
### and this function the return the dict which have additional two key values drive_path and drive_name

def get_new_name(item:dict) -> dict:
    path , ext = os.path.splitext(item['Path'])
    drive_path = f'{path}_({convert_to_utc(item['ModTime'])}){ext}'
    item['Drive_Path'] = drive_path
    return item

### this function do all the sorting for us

def get_sorted(source_list:list[dict],drive_list:list[dict]) -> list[list[dict]]:
    """It return  uploads_list , download_list ,  upload_size , download_size , number of modified files"""
    
    download_list = [] 

    upload_size , download_size , new_folders , modified_files = 0 , 0 , 0 , 0

    drive_set = set() 
    drive_set2 = {}
    upload_dict = {}
    drive_set_mod = set()

    def without_time(string:str) -> str:
        path , ext = os.path.splitext(string)
        path = path[0:len(path) - 22]
        return path+ext

    for item in drive_list:
        drive_set2[without_time(item['Path'])] = (without_time(item["Path"]),without_time(item["Name"]),item["Size"],item['ModTime'],item["IsDir"],item['Path'])

    for item in drive_list:
        if item['Path'] not in drive_set_mod:
            if item["Path"] in drive_set2:
                lists = list(drive_set2[item['Path']])
                drive_set_mod.add(lists.pop(-1))
                drive_set.add(tuple(lists))
            else:
                drive_set.add((item["Path"],item["Name"],item["Size"],item['ModTime'],item["IsDir"]))

    while source_list != [] : 
        item = source_list.pop(0)
        if item['IsDir'] is not True:
            time = convert_to_utc(item['ModTime'])
            if (item["Path"],item["Name"],item["Size"],time,item["IsDir"]) in drive_set :
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