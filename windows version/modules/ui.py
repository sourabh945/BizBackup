from tkinter import filedialog , messagebox

### modules imports 

from modules.file_operation import error
from modules.utils import list_remote

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
        
import tkinter as tk

def select_drive() -> str:
    """This function is for select the which rclone drive you wanted to used"""
    while True:
        remotes = list_remote()
        print('\nList of the remotes stores on the computer')
        for i , remote in enumerate(remotes):
            print(f'[{i}]  {remote}')
        inp = int(input("Enter the remote number >> "))
        if inp - 1 < len(remote):
            return remote[inp-1]
    