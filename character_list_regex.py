"""ecriture document personnage"""
import os
import re
characters_sheet = f"../../../annotations_fr-characters.csv"
dossier = "../corpus-items"

liste_exclue = ["DE", "MME", "MLLE", "M"]

def dramatis_personae(id_work):
    with open(characters_sheet, "r", encoding='utf8') as g,\
        open(f"{dossier}/{id_work}/{id_work}_characters.txt", "w", encoding="utf8") as f:
        character_list = [colonne[5].upper() for colonne in [line.rstrip().split(',') for line in g] if colonne[0] == id_work ]
        f.write(".*TOU(S|TES).*" +"\n" + "^(^| )(?<!' )[EÉÈÊéèê][NnM]? ?[Ss][EÉÈÊéèê][MN][BbRrNe][LlIiíÍïÏ][E]\W*" + "\n")
    
        chars = [c.split() for c in character_list]
        
        for c in chars:
            for name in c:
                if name not in liste_exclue:
                    
                    f.write(".*" + name + ".*" + "\n")
            


if __name__ == '__main__':
    idWork = "102"
    dramatis_personae(idWork)