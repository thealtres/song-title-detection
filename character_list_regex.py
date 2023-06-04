"""ecriture document personnage"""
import os
characters_sheet = f"../../../annotations_fr-characters.csv"
dossier = "../corpus-items"
def dramatis_personae(id_work):
    with open(characters_sheet, "r", encoding='utf8') as g,\
        open(f"{dossier}/{id_work}/{id_work}_characters.txt", "w", encoding="utf8") as f:
        character_list = [colonne[5].upper() for colonne in [line.rstrip().split(',') for line in g] if colonne[0] == id_work ]
        f.write(".*TOU(S|TES).*" +"\n" + "^(^| )(?<!' )[EÉÈÊéèê][NnM]? ?[Ss][EÉÈÊéèê][MN][BbRrNe][LlIiíÍïÏ][E]\W*" + "\n")
        for c in character_list:
            f.write(".*" + c + ".*" + "\n")
            


if __name__ == '__main__':
    idWork = "82"
    dramatis_personae(idWork)