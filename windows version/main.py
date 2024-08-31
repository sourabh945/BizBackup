import os 
from datetime import datetime as dt

import threading 
import queue
import subprocess

from colorama import Fore

from rclone_python import rclone



### this function handle all the upload using rclone also utilizing the multithreading and multiprocessing 

def upload(upload_dir:dict) -> dict:
    return_dict = {}

