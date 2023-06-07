"""
25 mai 2023
Lecture de fichier .txt pour le théâtre.
Compte le nombre d'acte et mentionne la derniere scene telle qu'elle apparait dans le doc txt.
La fonction de vérifaction écrit pour chaque idWork le type de la pièce avec le nombre d'acte écrit en toute lettre. 
NOTA : Si Acte 0, signifie qu'il y a seulement un acte ou qu'une mention de l'acte est faite avant la première scène. (ex 103, illustration sur page de couv)

"""


import re
import glob
import os
from config import dossier


SCENE = re.compile(r"(^| )\b(?<!' )SC[èEeÈ][Nn][Ee]\b")
PREMS = re.compile(r"PR[EèeÈÊê]MI[EèeÈÊê][Rr8][EèeÈÊê]\W?\b")
TYPE = re.compile(r"(COM[EÉÈÊéèê]DI[EÉÈÊéèê]|VAUD[EÉÈÊéèê]VILL[EÉÈÊéèê]|PI[EÉÈÊéèê]C[EÉÈÊéèê]).*[EÉÈÊéèê]N.*AC..[Ss]?")



def compte(liste_scenes):
    """
    Créé un dictionaire avec en clé le numéro de l'acte et en valeur la dernière scène de l'acte
        liste_scenes : liste contenant toutes les scènes identifiées dans le document
    """
    count_act = 0
    res = dict()
    for scene in liste_scenes:
        if PREMS.search(scene) or re.match(r"I\W?\b", scene[6:]):
            count_act += 1
        res[count_act] = scene
    return res
        

def extract(doc):
    """
    Extraction des scènes de la pièce via la regex SCENE. 
    """
    res_sc = []
    res_line = []
    with open(f"{doc}", "r", encoding="utf8") as f:
        count_line = 0
        for line in f:
            l = line.rstrip()
            count_line += 1
            if SCENE.search(l):
                res_sc.append( l.strip() + f" :{str(count_line)}:")
    return res_sc

def detection_type(doc):
    with open(f"{doc}", "r", encoding="utf8") as f2:
        res = []
        for line in f2:
            l = line.rstrip()
            if TYPE.search(l):
                res.append(l.strip())
        return res

def verif(id_work, csv):
    docs = glob.glob(f"{dossier}/{id_work}/*tesseract.txt")
    with open(csv, "a", encoding="utf8") as g:
        for d in docs:
            g.write(str(id_work) + ";" + ','.join(detection_type(d)) + ";" + str(compte(extract(d))) + "\n")

def verif_all(csv):
    ids = os.listdir(dossier)
    for id in ids:
        verif(id, csv)

if __name__ == '__main__':
    doc_sortie = "acts_sc1.csv"
    idWork = "103"
    #idWork = input("entrez id_work")
    verif(idWork, doc_sortie)
    #verif_all(doc_sortie)