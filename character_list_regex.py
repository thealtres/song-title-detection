"""écriture d'un document contenant les noms des personnages + ENSEMBLE et TOUSTES, avec modulation regex"""
import os
import re
from config import dossier
from config import characters_sheet
from config import dossier_sortie

liste_exclue = ["UN", "UNE","LE", "LA" ,"DE", "DES", "DU", "MME", "MLLE", "M", "MADAME", "MONSIEUR", "M.", "PREMIER", "DEUXIEME", "TROISIEME", "QUATRIEME", "CINQUIEME"]

def dramatis_personae(id_work):
    dossier_sortie_ecriture = f"{dossier}/{id_work}/{dossier_sortie}/"
    if not os.path.exists(dossier_sortie_ecriture):
            os.makedirs(dossier_sortie_ecriture)
    with open(f"{characters_sheet}", "r", encoding='utf8') as g,\
        open(f"{dossier_sortie_ecriture}/{id_work}_characters.txt", "w", encoding="utf8") as f:
        character_list = [colonne[1].upper() for colonne in [line.rstrip().split(',') for line in g] if colonne[0] == id_work ]
        f.write(".*TOU(S|TES).*" +"\n" + "^(^| )(?<!' )[EÉÈÊéèê][NnM]? ?[Ss][EÉÈÊéèê][MN][BbRrNe][LlIiíÍïÏ][E]\W*" + "\n")
        chars = [c.split() for c in character_list]
        for c in chars:
            for name in c:
                if name not in liste_exclue:
                    f.write(".*" + name + ".*" + "\n")