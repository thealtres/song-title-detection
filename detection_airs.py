""""
détection des airs et de leur nom et
enregistrement dans un document à part avec id de la pièce; id de l'air; titre.
       
""" 

import sys
import argparse
from os import listdir
from os.path import isfile, join
import re 
from fuzzywuzzy import process

from config import dossier
from config import airs_ref

parser = argparse.ArgumentParser()
parser.add_argument("id_work", type=int,
                    help="looks for couplet titles in id_work provided and writes them in new doc")


AIR = re.compile(r"(^| )\b(?<!' )([AâÂ] ?[IiïLlwmn][rRbBnNt])\W?\b")
AIR_extended = re.compile(r"^(^|\W)\b(?<!'\| )([AâÂÀáÁà] ?[IiïîÎtTLlrwmns1u] ?[rRbBnNtsa]?)\W*\b ?:?")
CHOEUR = re.compile(r"(^| )\b(?<!' )\b[Cc][Hh][OŒœ][EÉÈÊéèê]?[Uu][Rr]\b\W*")
ENSEMBLE = re.compile(r"^(^| )\b(?<!' )\b[EÉÈÊéèê][NnM]? ?[Ss][EÉÈÊéèê][MN][BbRrNe][LlIiíÍïÏ][E]\W*\b")
COUPLET = re.compile(r"^(^| )\b(?<!' )\b[Cc][Oo][Uu][Pp][IiïLltwmns1]?[Ee][TtlLIiï]\W?\b")
BIS = re.compile(r"\(bis\)")
TER = re.compile(r"\(ter\)")
FINALE = re.compile(r"^(^| )\b(?<!' )\b[FE][IiïLltwmns1][NMR][AâÂÀáÁà][LlIiíÍïÏ][EÉÈÊéèê]?\W?\b")
regex_filtra1 = [AIR_extended, CHOEUR,  COUPLET, FINALE]
#regex_filtra2 = [BIS, TER, ENSEMBLE]


def filtre(ligne, chaine):
    """
    Vérification manuelle par l'utilisateur du contenu de la chaine extraite par la regex
    le numéro de ligne a pour but d'aider à identifier les airs
    input [n] pour non
    """
    yn = input(f'''"{chaine}":{ligne}:      ''')
    if yn == 'n':
        return "n"
    else:
        return chaine

def extract(id_work):
    """Génère une liste qui contient les airs identifiées par les regex
    Ecriture dans un doc txt à part"""
    doc_entree = f"{dossier}/{id_work}/{id_work}_03_all-text_tesseract.txt"
    with open(doc_entree, "r", encoding="utf8") as f:
        res = []
        count_line = 0
        count_air = 0
        for line in f:
            count_line += 1
            l = line.rstrip()
            for r1 in regex_filtra1:
                if r1.search(l):    
                    air = filtre(count_line, l.strip())
                    if air != "n":
                        count_air += 1 
                        res.append(str(id_work) + ";" + str(count_air) + ";"+ str(process.extractOne(air, airs_ref)) + ';' + air + ";" + str(count_line))
        
    with open(f"{dossier}/{str(id_work)}/{str(id_work)}_airs.txt" , "w", encoding="utf8") as g:
        for r in res:
            g.write(r + "\n")

def extraction_dossier(dossier):
    docs = [d for d in listdir(dossier) if isfile(join(dossier, d))]
    for doc in docs:
        extract(doc)

with open(airs_ref, "r", encoding="utf8") as f:
    airs_ref = [ line.rstrip() for line in f ]

def suggest(id_work):
    "Suggests a title from the airs_ref document for an air found in the tesseract"
    doc_airs_id = f"{dossier}/{id_work}/{id_work}_airs.txt"
    try:
            open(doc_airs_id, "r")
    except FileNotFoundError as err : print(err)
    with open(doc_airs_id, "r", encoding='utf8') as g:
        airs_id = [colonne[3] for colonne in [ line.rstrip().split(';') for line in g] ]
        for a in airs_id:
            print(process.extractOne(a, airs_ref))

if __name__ == '__main__':
    args = parser.parse_args()
    id = args.id_work
    extract(id)

    