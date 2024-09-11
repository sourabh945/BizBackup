
from modules.f_ops import *
from modules.error import error
from modules.utils import *

from modules.configurator import configurator

def drive_check(drive_path:str):
    remote = drive_path.split(":")[0]
    remote += ":" 
    if remote not in remote_list():
        error(f'{remote} not in exists.')

def cal_size(list:list[dict]) -> float:
    size = 0
    for item in list:
        size += item['Size']
    return size/(1024*1024)


if __name__ == "__main__":

    print('[ Loading ] configurations ...')

    drive_path , source_path = configurator()

    check_paths(source_path)

    drive_check(drive_path)

    print(f"[ Output ] src: {source_path} remote: {drive_path}")

    print('[ Loading ] Indexing of files ...')

    source_list , drive_list =indexer(source_path,drive_path)

    print('[ Complete ] Indexing')

    print(f"\nTotal file in local : {len(source_list)}\nToal file in remote : {len(drive_list)}\n")


    is_empty_local = is_empty(source_list)
    is_empty_remote = is_empty(drive_list)

    if is_empty_local and not is_empty_remote:
        
        if input(f'The local folder is empty. To sync all the files from the remote of size {cal_size(drive_list)} MB , enter "y" and for cancel "n" : ').lower() == 'y':

            print("Start syncing the local...")
            if sync_local(source_path,drive_path):
                print('Sync Complete.')
                exit(0)
            else:
                print('Unable to complete sync.')
                exit(1)
        
        else:
            print('Cancelling all...')
            exit(0)
    
    elif not is_empty_local and is_empty_remote:
        
        if input(f'The remote folder is empty. To sync all the files from the remote of size {cal_size(drive_list)} MB , enter "y" and for cancel "n" : ').lower() == 'y':

            print("Start syncing the local...")
            if sync_remote(source_path,drive_path):
                print('Sync Complete.')
                exit(0)
            else:
                print('Unable to complete sync.')
                exit(1)
        
        else:
            print('Cancelling all...')
            exit(0)


    elif is_empty_local and is_empty_remote:
        print(f'\nBoth local {source_path} and remote {drive_path} are empty\n')
        exit(0)

    else:

        print('[ Loading ] sorting the files...')

        upload_list, download_list , upload_size , download_size , modified_files = get_sorted(source_list,drive_list)

        print('[ Complete ] Sorting')

        print('[ Result ]')



        print("Number of new created files in local : ",len(upload_list)-modified_files,"\n")

        print("Number of modified files  in local : ",modified_files,"\n")

        print("Number of deleted files in local : ",len(download_list,'\n'))

        print(f'Size of total upload : {upload_size/(1024*1024)} MB \n')

        print(f'Size of total deleted files : {download_size/(1024*1024)} MB \n')

        print('Select options: \n 1 > For upload only\n 2 > For download only\n 3 > For upload and download both\n 4 > Cancel\n')

        option = int(input("> "))

        if option == 4:
            print('Cancelling all ...')
            exit(0)
        elif option == 1:
            fails = runner(upload_file,upload_list,source_path,drive_path)
            if len(fails) == 0 :
                print('[ Complete ] uploading...')
                exit(0)
            else:
                print("File don't get uploades ")
                for item in fails:
                    print(item['Path'])
                exit(1)
        elif option == 2:
            fails = runner(download_file,download_list,source_path,drive_path)
            if len(fails) == 0 :
                print('[ Complete ] downloading...')
                exit(0)
            else:
                print("File don't get downloaded ")
                for item in fails:
                    print(item['Path'])
                exit(1)
        
        elif option == 3:
            if input("[ Caution ] Modified file are reverted in local. if yes enter 'y' and for no enter 'n' ").lower() == 'y':
                fails = runner(upload_file,upload_list,source_path,drive_path)
                if len(fails) == 0 :
                    print('[ Complete ] uploading...')
                else:
                    print("File don't get uploades ")
                    for item in fails:
                        print(item['Path'])
                    exit(1)
                fails = runner(download_file,download_list,source_path,drive_path)
                if len(fails) == 0 :
                    print('[ Complete ] downloading...')
                    exit(0)
                else:
                    print("File don't get downloaded ")
                    for item in fails:
                        print(item['Path'])
                    exit(1)