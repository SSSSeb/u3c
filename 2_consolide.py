import os
import time
import glob
import commun

from datetime import datetime

from pathlib import Path
from playsound import playsound

URA_DIRECTORY = Path(os.environ["U3C_URA_DIR"])

SYNTHESE_PREFIX = "pour_Franck"
SYNTHESE_TEMPO = Path("pour_Franck.tmp.txt")
BEEP_FILE = os.environ["U3C_BEEP_FILE"]

T0_FILE = os.environ["U3C_T0_FILE"]
# prise en compte des 10 secondes environ de délais entre le vrai timing
# et le temps pour scanner...
# DELTA_T = os.environ["U3C_DELTA_T"]

nb_rfid_prev = 0

if not URA_DIRECTORY.exists() or not URA_DIRECTORY.is_dir():
    print(f"le dossier {URA_DIRECTORY} n'existe pas ou n'est pas un répertoire")
    exit(1)

rfids2doss,nb_rfids_inscrits,rfids_inscrits,coureurs = commun.verif_inscriptions_rfid()

nb_rfids_vus = 0

with open(T0_FILE, "r") as f:
    t0val = f.read().strip()

try:
    t0 = datetime.strptime(t0val, "%H:%M:%S")
except ValueError:
    print(f"impossible de convertir l'horaire de départ du CROSS à partir de {T0_FILE}")
    exit(1)

print(f"t0={t0}")
# en admettant que tout le monde passe la ligne cette boucle s'arrètera toute seule
# sinon elle attendra indéfiniment le passage des derniers RFIDs

nb_rfids_deja_imprimes = 0
cur_dossards_vus = ""
cur_doss_vus = set()

while nb_rfids_vus < nb_rfids_inscrits:

    nb_rfids_vus = 0
    seen = set()
    ordered_files = sorted(glob.glob(str(URA_DIRECTORY) + "/ura.??????.txt"))
    # print(sorted_files)

    with open(SYNTHESE_TEMPO, "w") as synthese_tmp_f:
        # ligne d'entete importante pour le logiciel de Franck.
        synthese_tmp_f.write(
            "NOM\tPRENOM\tSEXE\tNAISSANCE\tNUMERO\tTEMPS\tCOURSE\tDISTANCE\tVILLE\tEMAIL\tCLUB\tLICENCE\n"
        )
        for curf in ordered_files:
            # print(f"j'ouvre le fichier {curf}")
            with open(curf, "r") as file:
                for line in file:
                    # E280689400005003EA7498AA	06:01:43.657  	-53	1
                    line = line.strip()
                    line_fields = line.split()
                    rfid_cand = line_fields[0].strip()
                    # print(f"rfid_cand={rfid_cand}")
                    if rfid_cand not in seen:
                        # print("not seen "+rfid_cand)
                        seen.add(rfid_cand)
                        if rfid_cand in rfids_inscrits:
                            rfid = rfid_cand
                            # print(f"go {rfid} {timing} \n")
                            cur_temps = line_fields[1]
                            cur_dos = rfids2doss[rfid]
                            cur_cour = coureurs[cur_dos]
                            # print(cur)
                            # print(f"arrivée du dossard {cur_dos}")
                            # print(f"arrivée de {coureurs[cur_dos]['nom']}")
                            tf = datetime.strptime(cur_temps, "%H:%M:%S.%f")
                            delta = tf - t0
                            synthese_tmp_f.write(
                                f"{cur_cour['nom']}\t{cur_cour['prénom']}\t{cur_cour['genre']}\t{cur_cour['date_de_naissance']}\t{cur_dos}\t{delta}\t{cur_cour['cross']}\t{cur_cour['km']}\t{cur_cour['village']}\t{cur_cour['email']}\t{cur_cour['club']}\t{cur_cour['license']}\n"
                            )
                            nb_rfids_vus = nb_rfids_vus + 1
                            if cur_dos not in cur_doss_vus:
                                cur_dossards_vus = (
                                    cur_dossards_vus + "[" + str(cur_dos) + "]"
                                )
                                cur_doss_vus.add(cur_dos)

    if nb_rfids_vus > nb_rfids_deja_imprimes:
        dest_f_idx = Path(SYNTHESE_PREFIX + str(nb_rfids_vus) + ".txt")
        dest_f = Path(SYNTHESE_PREFIX + "_cur" + ".txt")
        os.replace(SYNTHESE_TEMPO, dest_f_idx)
        if os.path.exists(dest_f):
            os.remove(dest_f)
        os.symlink(dest_f_idx, dest_f, target_is_directory=False)
        # print(nb_rfids)
        # print(f"{nb_rfids-nb_rfids_found} beeps...")
        print(cur_dossards_vus, end="", flush=True)
        print(f"#{nb_rfids_vus}", end="", flush=True)
        cur_dossards_vus = ""
        for i in range(nb_rfids_vus - nb_rfids_deja_imprimes):
            # print("X", end="", flush=True)
            playsound(BEEP_FILE, block=True)
            time.sleep(0.02)
        nb_rfids_deja_imprimes = nb_rfids_vus
    print(".", end="", flush=True)
    time.sleep(0.01)

print(f"cross terminé, {nb_rfids_vus} RFIDS détectés...")
exit(0)
