import json 
from rclone_python import rclone
import os
import datetime as dt

source_path = ''
drive_path = ''

try:
    os.system(f'rclone lsjson -R {source_path} >> ./source.json')
    os.system(f'rclone lsjson -R {drive_path}>> ./target.json')

except Exception as error:
    print(error)

source_data = []
target_data = []

try:
    with open("./.rclone_logs/source.json","r") as file:
        source_data = json.load(file)
        file.close()

    with open("./.rcloen_logs/target.json","r") as file:
        target_data = json.load(file)
        file.close()



except Exception as error:
    print(error)

if target_data.__len__() == 0:
    print("No file present at the target")
    size_of_upload  =0 
    print(f'Total number of uploads are :: {source_data.__len__()}')
    for file in source_data:
        size_of_upload = size_of_upload + file['Size']
    print(f"Total size of upload is :: {size_of_upload/1024}")
    if (input("Enter the y for confirm to upload \n and for cancel press any enter anykey::")).lower() == 'y':
        rclone.sync(src_path=source_path,dest_path=drive_path,show_progress=True)
    else :
        exit()

print(f"Files in source : {source_data.__len__()}")
print(f"Files in drive : {target_data.__len__()}")

new_files = []
diff_extension_files  = []
modified_files = []

print("New files are :: ")

size_of_upload = 0

for source in source_data:

    is_done = False

    for target in target_data:
        if source['Path'] == target['Path']:
            if source['Size'] == target['Size'] :
                if source['ModTime'].split("T")[0] == target['ModTime'].split("T")[0] or source['IsDir'] is True:
                    if(source['MimeType'] == target['MimeType'] or source['MimeType'].split(";")[0] == target['MimeType']):
                        is_done = True
                        target_data.remove(target)
                        break
                    else:
                        is_done = True
                        temp = [source,target]
                        diff_extension_files.append(temp)
                        target_data.remove(target)
                        break
            else:
                modified_files.append(source)
                is_done = True
                target_data.remove(target)
                break

    if is_done is False:
        new_files.append(source)
        print(source['Path'])
        size_of_upload = int(source['Size']) + size_of_upload


print(f'New files in the source :: {len(new_files)}')

print('Modified Files are')

for file in modified_files:
    print(file['Path'])
    size_of_upload = int(file['Size']) +size_of_upload

print(f"Total upload Size is :: {size_of_upload/1024}MB")

if input("Enter y to confirm to upload \n for cancel press any key ") == 'y':
    try:
        print("Uploading the new files :: ")
        for file in new_files:
            rclone.copy(in_path=source_path+file['Path'],out_path=drive_path+file['Path'],show_progress=True,ignore_existing=True)
        print("Upload complete")
        print("Uploading the modified files : ")
        time = str(dt.datetime.now())
        for file in modified_files:
            rclone.copy(in_path=source_path+file['Path'],out_path=drive_path+file['Path']+f"({time})",show_progress=True,ignore_existing=True)
        print("Upload complete")
        print(f'Number of the confict :: {diff_extension_files.__len__()}')
        if diff_extension_files.__len__() != 0:
            with open("./Confict.json",'r') as file:
                writer = json.dumps(diff_extension_files) 
                file.write(writer)
            print("All confict are save in json files with there copy in the drive")
    except Exception as error:
        print(error)

        
else:
    exit()


        

