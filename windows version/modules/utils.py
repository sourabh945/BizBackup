import subprocess 

def run_cmd(command:str) -> subprocess.CompletedProcess:
    cmd = [word  for word in command.split(' ') if word != ""]
    return subprocess.run(cmd,capture_output=True,text=True,shell=True)

