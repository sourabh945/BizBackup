import asyncio


from modules.f_ops import *
from modules.error import error
from modules.utils import runner , uploader, sync_local , sync_remote , script_finder , indexer , download_file

from modules.configurator import *

def cal_size(list:list[dict]) -> float:
    size = 0
    for item in list:
        size += item['Size']
    return size/(1024*1024)

def length(list:list[dict]) -> int:
    count = 0 
    for item in list:
        if item['IsDir'] is False:
            count += 1
    return count 


if __name__ == "__main__":

    print('[ Loading ] configurations ...')

    drive_path , source_path = configurator()

    log_folder , logs_path , fails_path , sleep_time = advance_config_loader()

    logs_path = log_folder + "/" + os.path.basename(logs_path)

    fails_path = log_folder + "/" + os.path.basename(fails_path)

    log_maker(log_folder,logs_path,fails_path)

    scripts_writer()

    print('[ Complete ] configurations')

    print(f"[ Output ] src: {source_path} remote: {drive_path}")

    print('[ Loading ] Indexing of files ...')

    source_list , drive_list =indexer(source_path,drive_path)

    print('[ Complete ] Indexing')

    print(f"\nTotal file in local : {length(source_list)}\nToal file in remote : {length(drive_list)}\n")


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

        if not upload_list and not download_list :
            print("\nEverything is up-to-date\n")
            exit(0)

        print('[ Result ]')

        print("Number of new created files in local : ",len(upload_list)-modified_files,"\n")

        print("Number of modified files  in local : ",modified_files,"\n")

        print("Number of deleted files in local : ",len(download_list),'\n')

        print(f'Size of total upload : {upload_size/(1024*1024)} MB \n')

        print(f'Size of total deleted files : {download_size/(1024*1024)} MB \n')

        print('Select options: \n 1 > For upload only\n 2 > For download only\n 3 > For upload and download both\n 4 > Cancel\n')

        option = int(input("> "))


        if option == 4:
            print('Cancelling all ...')
            exit(0)


        elif option == 1:
            output_file = script_finder('upload')
            fails = asyncio.run(uploader(upload_list,source_path,drive_path,output_file,sleep_time,logs_path,fails_path))
            if len(fails) == 0 :
                print('[ Complete ] uploading...')
                exit(0)
            else:
                print("File don't get uploades ")
                for item in fails:
                    print(item)
                exit(1)


        elif option == 2:
            output_file = script_finder('downlaod')
            fails = runner(download_file,download_list,source_path,drive_path,output_file,logs_path,fails_path)
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
                output_file = script_finder('upload')
                fails = asyncio.run(uploader(upload_list,source_path,drive_path,output_file,sleep_time,logs_path,fails_path))
                if len(fails) == 0 :
                    print('[ Complete ] uploading...')
                else:
                    print("File don't get uploades ")
                    for item in fails:
                        print(item)
                    exit(1)
                output_file = script_finder('donwload')
                fails = runner(download_file,download_list,source_path,drive_path,output_file,logs_path,fails_path)
                if len(fails) == 0 :
                    print('[ Complete ] downloading...')
                    exit(0)
                else:
                    print("File don't get downloaded ")
                    for item in fails:
                        print(item['Path'])
                    exit(1)