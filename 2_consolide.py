import subprocess
import platform
import os
import socket
import time

from pathlib import Path

URA_DIRECTORY = Path(os.environ["U3C_URA_DIR"])
FICHIER_RFIDS_DOSSARDS = Path(os.environ["U3C_RFIDS_FILE"])


nb_rfid_prev=0

if not URA_DIRECTORY.exists() or not URA_DIRECTORY.is_dir():
    print(f"le dossier {URA_DIRECTORY} n'existe pas ou n'est pas un répertoire")
    exit(1)

with open(FICHIER_RFIDS_DOSSARDS,'r') as file:
    rfids_dossards = []
    for line in file:
        line = line.strip()
        line_fields = line.split(' ')
        rfids_dossards.append(line_fields)

nb_rfids_total=len(rfids_dossards)
print(f"{nb_rfids_total} entrées dans le fichier de RFIDS/DOSSARDS")
