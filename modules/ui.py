# from tkinter import filedialog , messagebox


### modules imports 

from modules.error import error
from modules.utils import remote_list , get_folders

# def select_folder():
#     try:
#         print('Select the folder which you wanted to backup,')
#         selection = filedialog.askdirectory()
#         if selection is not None:
#             return selection 
#         else:
#             messagebox.showerror('Error','No folder is selected')
#             error('No folder is selected')
#             exit(1)
#     except Exception as err:
#         error(err)

def select_folder():
    print("Enter the path of the backup folder : \n")
    path = input("> ")
    return path

def select_drive() -> str:
    """This function is for select the which rclone drive you wanted to used"""
    remotes = remote_list()
    while True:
        if not remotes :
            error('No remote is found. Please make a new remote.')
        print('\nList of the remotes stores on the computer')
        for i , remote in enumerate(remotes):
            print(f'[{i+1}]  {remote}')
        inp = int(input("Enter the remote number >> "))
        if inp - 1 < len(remotes) and inp > 0:
            return remotes[inp-1]
        else:
            print("Please enter the valid number !!! ")
    
def select_remote_folder(drive_name:str) -> str:

    print('[ Loading ] folders in selected remote ')

    folders = get_folders(drive_name) 

    print("[ Complete ] folders fetched")

    print("Select the backup folder in remote : ")

    while True:

        if not folders :
            error(f'No folder is found in the remote {drive_name}')

        for i , folder in enumerate(folders):
            print(f'{i+1} > {folder}')

        sel = int(input(" Enter the remote number >> ")) 

        if sel - 1 < len(folders) and sel > 0:
            return folders[sel -1]
        else:
            print('Please enter the valid number !!! ')
