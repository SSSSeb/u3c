import subprocess
import platform
import os
import socket
import time

from pathlib import Path

URA_DIRECTORY = os.environ['U3C_URA_DIR']
JADAK_IP = os.environ['U3C_JADAK_IP']
JADAK_PORT= os.environ['U3C_JADAK_PORT']

def is_port_open(ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        timeout = 1
        s.settimeout(timeout)
        try:
                s.connect((ip, int(port)))
                s.shutdown(socket.SHUT_RDWR)
                return True
        except:
                return False
        finally:
                s.close()

def is_binary_exist(binary_name: str) -> bool:
    if platform.system() == "Windows":
        try:
            subprocess.run(['where', binary_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            return False
    else:
        try:
            subprocess.run(['which', binary_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            return False

for binary in ['ping','netcat']:
    if is_binary_exist(binary):
        print(f'{binary} found')
    else:
        print(f'{binary} not found')
        exit

index = 1

while True:
    while True:
        path = Path(URA_DIRECTORY)
        path.mkdir(parents=True, exist_ok=True)
        path = Path(URA_DIRECTORY+".err")
        path.mkdir(parents=True, exist_ok=True)
        cur_file = Path(URA_DIRECTORY + "/ura." + str(index))
        cur_err_file = Path(URA_DIRECTORY + ".err/ura." + str(index) + ".err")
        if cur_file.exists():
            print(Path +" already exists...")
            index=index+1
        else:
             break

    print("(re) connection à URA ->" + str(cur_file))
    print("connection vers " + JADAK_IP +':'+JADAK_PORT)
    while True:
        if is_port_open(JADAK_IP,JADAK_PORT):
             print("service JADAK semble dispo...")
             break
        print(".",end='',flush=True)
        time.sleep(1)

    args = [ "nc", JADAK_IP, JADAK_PORT ]

    subprocess.run()
