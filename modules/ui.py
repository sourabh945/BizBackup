from tkinter import filedialog , messagebox


### modules imports 

from modules.error import error
from modules.utils import remote_list

def select_folder():
    try:
        print('Select the folder which you wanted to backup,')
        selection = filedialog.askdirectory()
        if selection is not None:
            return selection 
        else:
            messagebox.showerror('Error','No folder is selected')
            error('No folder is selected')
            exit(1)
    except Exception as err:
        error(err)
        

def select_drive() -> str:
    """This function is for select the which rclone drive you wanted to used"""
    while True:
        remotes = remote_list()
        if not remotes :
            error('No remote is found. Please make a new remote.')
        print('\nList of the remotes stores on the computer')
        for i , remote in enumerate(remotes):
            print(f'[{i}]  {remote}')
        inp = int(input("Enter the remote number >> "))
        if inp - 1 < len(remote):
            return remote[inp-1]
    