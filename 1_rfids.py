import subprocess
import platform
import os
import socket
import time

from pathlib import Path

URA_DIRECTORY = os.environ["U3C_URA_DIR"]
JADAK_IP = os.environ["U3C_JADAK_IP"]
JADAK_PORT = os.environ["U3C_JADAK_PORT"]


def is_port_open(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    timeout = 3
    s.settimeout(timeout)
    try:
        s.connect((ip, int(port)))
    except Exception as e:
        print(e)
        return False
    s.shutdown(socket.SHUT_RDWR)
    s.close()
    return True

def is_binary_exist(binary_name: str) -> bool:
    if platform.system() == "Windows":
        try:
            subprocess.run(
                ["where", binary_name],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            return True
        except subprocess.CalledProcessError:
            return False
    else:
        try:
            subprocess.run(
                ["which", binary_name],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            return True
        except subprocess.CalledProcessError:
            return False


for binary in ["ping", "ncat"]:
    if is_binary_exist(binary):
        print(f"{binary} found")
    else:
        print(f"{binary} not found")
        exit(1)

index = 1

while True:
    while True:
        path = Path(URA_DIRECTORY)
        path.mkdir(parents=True, exist_ok=True)
        path = Path(URA_DIRECTORY + ".err")
        path.mkdir(parents=True, exist_ok=True)
        cur_file = Path(URA_DIRECTORY + "/ura." + str(index) + ".txt")
        cur_err_file = Path(URA_DIRECTORY + ".err/ura." + str(index) + ".err")
        if cur_file.exists():
            # print(path.__str__ +" already exists...")
            index = index + 1
        else:
            break


    print("(re) connection à URA ->" + str(cur_file))
    print("connection vers " + JADAK_IP + ":" + JADAK_PORT)
    while True:
        if is_port_open(JADAK_IP, JADAK_PORT):
            print("service JADAK semble dispo...")
            break
        print(".", end="", flush=True)
        time.sleep(1)

    command = "ncat " + JADAK_IP + " " + JADAK_PORT + " >" + str(cur_file)

    try:
        result = subprocess.run(command, check=True, shell=True)
    except FileNotFoundError:
        print(f"command {command} non trouvée...")
        exit(1)
    except subprocess.CalledProcessError as error:
        print(f"problème pour lancer la commande de type ncat: {error} ")
        time.sleep(1)
