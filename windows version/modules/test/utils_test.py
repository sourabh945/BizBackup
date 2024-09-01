from utils import run_cmd

print(run_cmd('dir',shell=True).stdout)

print(run_cmd('rclone version').returncode)

print(run_cmd('ls',shell=True).stderr)

print(run_cmd('rclone listremotes',inputs=['sourabh']))
