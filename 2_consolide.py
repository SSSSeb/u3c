import subprocess
import platform
import os
import socket
import time
import glob
import re

# import pygame

from pathlib import Path
from playsound import playsound

URA_DIRECTORY = Path(os.environ["U3C_URA_DIR"])
FICHIER_RFIDS_DOSSARDS = Path(os.environ["U3C_RFIDS_FILE"])
SYNTHESE = Path("synthese_rfids_timings.txt")
SYNTHESE_TEMPO = Path("synthese_rfids_timings.tmp.txt")
BEEP_FILE = os.environ["U3C_BEEP_FILE"]

# pygame.init()
# beep = pygame.mixer.Sound(BEEP_FILE)


nb_rfid_prev = 0

if not URA_DIRECTORY.exists() or not URA_DIRECTORY.is_dir():
    print(f"le dossier {URA_DIRECTORY} n'existe pas ou n'est pas un répertoire")
    exit(1)

with open(FICHIER_RFIDS_DOSSARDS, "r") as file:
    rfids_dossards = []
    rfids = []
    for line in file:
        line = line.strip()
        line_fields = line.split(" ")
        rfids.append(line_fields[0])
        rfids_dossards.append(line_fields)

nb_rfids_system = len(rfids_dossards)
print(f"{nb_rfids_system} entrées dans le fichier de RFIDS/DOSSARDS")
# print(rfids)
rfids_pattern = re.compile("|".join(rfids))
nb_rfids_found = 0
# print(f"{nb_rfids_found} rfids found")
while True:
    seen = set()
    ordered_files = sorted(glob.glob(str(URA_DIRECTORY) + "/ura.???.txt"))
    # print(sorted_files)
    list = []
    with open(SYNTHESE_TEMPO, "w") as synthese_tmp:
        for curf in ordered_files:
            with open(curf, "r") as file:
                for line in file:
                    line = line.strip()
                    line_fields = line.split()
                    rfid_cand = line_fields[0]
                    if rfid_cand not in seen:
                        # print("not seen "+rfid_cand)
                        seen.add(rfid_cand)
                        if re.match(rfids_pattern, rfid_cand):
                            rfid = rfid_cand
                            # print(f"go {rfid} {timing} \n")
                            timing = line_fields[1]
                            item = (rfid, timing)
                            list.append(item)
                            synthese_tmp.write(rfid + " " + timing + "\n")
    if os.path.exists(SYNTHESE):
        os.remove(SYNTHESE)
    os.rename(SYNTHESE_TEMPO, SYNTHESE)
    nb_rfids = len(list)
    # print(list)
    # print(nb_rfids)
    # print(f"{nb_rfids-nb_rfids_found} beeps...")
    for i in range(nb_rfids - nb_rfids_found):
        print("X", end="", flush=True)
        playsound(BEEP_FILE, block=True)
        time.sleep(0.02)
    nb_rfids_found = nb_rfids
    print(".", end="", flush=True)
    time.sleep(0.01)
