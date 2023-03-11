import os
import shutil
import commun
import time
from datetime import datetime

INSCR_FILE = os.environ["U3C_INSCRIPTIONS"]
RFID_FILE = os.environ["U3C_RFIDS_FILE"]
BEEP_FILE = os.environ["U3C_BEEP_FILE"]
T0_FILE = os.environ["U3C_T0_FILE"]
URA_DIRECTORY = os.environ["U3C_URA_DIR"]
RES_DIRECTORY = os.environ["U3C_RES_DIR"]

# test necessary files exist

for fichier in [INSCR_FILE, RFID_FILE]:
    if not os.path.isfile(fichier):
        print("fichier manquant:", fichier)
        exit(1)

commun.verif_inscriptions_rfid()

with open(INSCR_FILE, "r") as inscriptions:
    # for line in inscriptions:
    #    print(line)
    lignes = inscriptions.readlines()

coureurs = []

for line in lignes:
    coureurs.append(line.split())

nb_runners = len(coureurs)

print("")
print("***")
print("*** trouvé", nb_runners, "coureurs dans", INSCR_FILE)
print("***")
print("")

# montrer les dix premiers coureurs et les 10 derniers du fichier.

for idx in range(0, 2):
    print("#", idx + 1, ":", coureurs[idx][1], ",", coureurs[idx][0])
print("...")
print("...")
for idx in range(nb_runners - 2, nb_runners):
    print("#", idx + 1, ":", coureurs[idx][1], ",", coureurs[idx][0])

with open(RFID_FILE, "r") as rfids:
    lignes = rfids.readlines()

rfids = []

for line in lignes:
    rfids.append(line.split())

nb_rfids = len(rfids)

print("")
print("***")
print("*** trouvé", nb_rfids, "rfids dans", RFID_FILE)
print("***")
print("")

for idx in range(0, 2):
    print("#", idx + 1, ":", rfids[idx][1], ",", rfids[idx][0])
print("...")
print("...")
for idx in range(nb_rfids - 2, nb_rfids):
    print("#", idx + 1, ":", rfids[idx][1], ",", rfids[idx][0])

print("")
print("***")
print("*** test du beep")
print("***")
print("")

b=commun.initialise_beep()

reponse = input("appuyer sur Entree pour tester le son (ou 'N' pour ne pas le faire)")
if reponse != "N":
    for i in range(0,5):
        print(f"#{i}",end="",flush=True)
        commun.beep(b,300)
    for i in range(0,5):
        print(f"#{i}",end="",flush=True)
        commun.beep(b,100)
    print("test du son (10 bips en rafale, deux vitesses...) terminé")

print("")
print("*** appuyer sur ENTREE au démarrage de la course")
print("*** ceci effacera les fichiers de précédentes courses dans", URA_DIRECTORY)
print("*** et consigne l'heure exacte du démarrage dans le fichier", T0_FILE)

ignore = input("*** appuyer sur Entree pour démarrer la course...")

maintenant = datetime.now()

print("")
print("***")
print("*** t0: démarrage de la course à: ", maintenant.strftime("%H:%M:%S"))
print("***")
print("écriture du fichier de date dans", T0_FILE,"\n")

with open(T0_FILE, "w") as fichier_t0:
    fichier_t0.write(maintenant.strftime("%H:%M:%S") + "\n")

print("\n")
print("*** \n")
reponse = input(
    f"ATTENTION, CONFIRMER PAR 'oui' POUR EFFACEMENT DE {URA_DIRECTORY} ? (oui/NON)"
)

if reponse == "oui":
    # if directory can not be deleted ... you should warn instead...
    shutil.rmtree(URA_DIRECTORY, ignore_errors=True)
    shutil.rmtree(RES_DIRECTORY, ignore_errors=True)
else:
    print("\n\n*** repertoire NON EFFACE... course déjà en cours ?")
