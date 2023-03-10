import os
from pathlib import Path

def verif_inscriptions_rfid():

    INSCR_FILE = os.environ["U3C_INSCRIPTIONS"]
    FICHIER_RFIDS_DOSSARDS = Path(os.environ["U3C_RFIDS_FILE"])

    for fichier in [INSCR_FILE, FICHIER_RFIDS_DOSSARDS]:
        if not os.path.isfile(fichier):
            print("fichier manquant:", fichier)
            exit(1)

    with open(INSCR_FILE, "r") as inscriptions_file:
        # for line in inscriptions:
        #    print(line)
        # sauter la premiere ligne pour Franck
        inscriptions = inscriptions_file.readlines()[1:]
        # DUPONT JEAN-CHRISTOPHE H       1959    691             CROSS LONG      10      POISAT  toto@voila.fr  RIA Champagnier

    coureurs = {}

    dossards_inscrits = set()
    rfids2doss = {}

    for line in inscriptions:
        cur_l = line.split("\t")
        cur_doss = cur_l[4]
        if cur_doss in dossards_inscrits:
            print(f"deux dossards {cur_doss} trouvés")
            exit(1)
        coureurs[cur_doss] = {
            "nom": cur_l[0].strip(),
            "prénom": cur_l[1].strip(),
            "genre": cur_l[2].strip(),
            "date_de_naissance": cur_l[3].strip(),
            "cross": cur_l[6].strip(),
            "km": cur_l[7].strip(),
            "village": cur_l[8].strip(),
            "email": cur_l[9].strip() if len(cur_l) > 9 else "",
            "club": cur_l[10].strip() if len(cur_l) > 10 else "",
            "license": cur_l[11].strip() if len(cur_l) > 11 else "",
        }
        dossards_inscrits.add(cur_doss)
        # print(f"ajout du dossard {cur_doss}")


    with open("table_coureurs_debug.txt", "w") as out:
        for elem in coureurs:
            out.write(f"{coureurs[elem]}\n")


    with open(FICHIER_RFIDS_DOSSARDS, "r") as file:
        # RFIDS des gens inscrits
        rfids_inscrits = []
        # RFIDS connus par le systeme
        dossards_systeme = set()
        for line in file:
            line = line.strip()
            line_fields = line.split(" ")
            cur_rfid = line_fields[0]
            cur_doss = line_fields[1]
            if cur_doss in dossards_inscrits:
                rfids_inscrits.append(cur_rfid)
                rfids2doss[cur_rfid] = cur_doss
            dossards_systeme.add(cur_doss)

    nb_rfids_inscrits = len(rfids_inscrits)
    print(f"{nb_rfids_inscrits} RFIDS d'inscrits enregistrés")

    with open("rfids_inscrits_debug.txt", "w") as file:
        for element in rfids_inscrits:
            file.write(element + "\n")

    for dossard in dossards_inscrits:
        if dossard not in dossards_systeme:
            print(f"dossard {dossard} n'existe pas dans {FICHIER_RFIDS_DOSSARDS}")
            exit(1)

    if len(dossards_inscrits) != len(rfids_inscrits):
        print(f"nb inscrit {dossards_inscrits} different de nb rfids {rfids_inscrits}")
        exit(1)

    return rfids2doss,nb_rfids_inscrits,rfids_inscrits,coureurs
