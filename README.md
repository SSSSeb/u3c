# u3c

code de chronometrage pour le cross de champagnier

- necessite (windows 64 bit) JADAK URA configuré pour exporter les RFIDS en http 9055
- voir fichier "reglages" pour les adresses IPs 
- sftp://seb@192.168.0.2 sur le PC de FRANCK

architecture:

- 0_init: verifie les fichiers d'inscriptions et de RFIDS -> DOSSARDS puis verifie que le BEEP fonctionne

(!) virer les lignes blanches ou pleines de \t mais sans données

- 1_rfids: demon qui se reconnecte à l'URA et recopie tous les scans dans le dossier ./ura... capable de se reconnecter et de créer un nouveau fichier à chaque reconnection

- 2_consolide: fusionne et dédoublonne les fichiers URA pour en faire un seul avec les entrees dédupliquées et uniquement les dates d'arrivées

- 3_synthese: fabrique un fichier d'arrivées avec les temps de course

tableau.sh: à tourner en boucle pour avoir un état des 30 dernières arrivées...
