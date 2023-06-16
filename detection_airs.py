""""
Alexia Schneider juin 2023
détection des airs et de leur titre
output: [id_work]_airs.txt dans le dossier id_work du corpus Thealtres
id_work; id_air; titre_suggéré ; titre_extrait ; ligne ; isair 
avec id_work : entré par l'utilisateur en ligne de commande
id_air : incrémenté pour la pièce
titre_extrait : ligne contenant un titre candidat
ligne : ligne dans le document OCR_tesseract. 
titre_suggéré  : string matching depuis la liste de titres de référence fournie par Lara Nugues
isair : booléen, 1 pour air. 
       
""" 

import sys
import argparse

import re 
from fuzzywuzzy import process
import difflib

from config import dossier
from config import airs_ref
import character_list_regex

parser = argparse.ArgumentParser()
parser.add_argument("id_work", type=int,
                    help="gives candidates in id_work provided and writes them in new doc >  input 'n' to reject the line, anything else to add it")

AIR_extended = re.compile(r"^(^|\W)\b(?<!'\| )([AâÂÀáÁà] ?[IiïîÎtTLlrwmns1u] ?[rRbBnNtsa]?)\W*\b ?:?")
CHOEUR = re.compile(r"^(^|\W)\b(?<!\|' )\b[Cc][Hh][OŒœ][EÉÈÊéèê]?[Uu][Rr]\b\W*")
COUPLET = re.compile(r"^(^|\W)\b(?<!' )\b[Cc][Oo][Uu][Pp][IiïLltwmns1]?[Ee][TtlLIiï]\W?\b")
FINALE = re.compile(r"^(^|\W)\b(?<!' )\b[FE][IiïLltwmns1][NMR][AâÂÀáÁà][LlIiíÍïÏ][EÉÈÊéèê]?\W?\b")
regex_filtra1 = [AIR_extended, CHOEUR,  COUPLET, FINALE]

AIR_seul = re.compile(r"(^| )(?<!' )\w+\W*\s*\b")
stage_directions = re.compile(r"^(^| )[\{\(].*[\}\)]?")

#BIS = re.compile(r"\(bis\)")
#TER = re.compile(r"\(ter\)")
#ENSEMBLE = re.compile(r"^(^| )\b(?<!' )\b[EÉÈÊéèê][NnM]? ?[Ss][EÉÈÊéèê][MN][BbRrNe][LlIiíÍïÏ][E]\W*\b")
#regex_filtra2 = [BIS, TER, ENSEMBLE]

def extract(id_work):
    """Produces a list containing idWork;idAir;ocrAir;ocrLine;suggestedTitle;isair
    written in a idWork_airs.txt doc in corresponding directory"""
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
                    air = isair(l.strip(), count_line)
                    if air[1] == "1":
                        count_air += 1 
                        titre = air[0]
                        if r1.fullmatch(str(air[0])):
                            titre = next(f) 
                            while cherche_titre(titre, id_work) == False:
                                titre = next(f)   
                            res.append(str(id_work) + ";" + str(count_air) + ";"+   str(air[0])+ ':' + str(titre.rstrip()) + ";" + str(count_line)  + ";" + str(suggest(titre.rstrip())) + ";" + str(air[1]))
                        else:
                            res.append(str(id_work) + ";" + str(count_air) + ";"+ str(titre) + ';' + str(count_line) + ";" + str(suggest(titre)) + ";" + str(air[1]))
                    else:
                        res.append(str(id_work) + ";;" + str(air[0]) + ";" + str(count_line) + ";;" + str(air[1]))
    with open(f"{dossier}/{str(id_work)}/{str(id_work)}_airs.csv" , "w", encoding="utf8") as g:
        for r in res:
            g.write(r + "\n")


def isair(chaine, ligne):
    """
    Vérification manuelle par l'utilisateur du contenu de la chaine extraite par la regex
    le numéro de ligne a pour but d'aider à identifier les airs
    input [n] pour non
    """
    yn = input(f'''"{chaine}":{ligne}:      ''')
    if yn == 'n':
        return chaine, "0"
    else:
        return chaine, "1"

def cherche_titre(chaine, id_work):
    with open(f"{dossier}/{id_work}/{id_work}_characters.txt", "r", encoding="utf8") as f:
        character_list = [ line.rstrip() for line in f ]
        for c in character_list:
            if re.search(c, chaine):
                return False
    if re.fullmatch(r"(\n|\s+)", chaine):
        return False
    if stage_directions.search(chaine):
        return False
    else:
        return True

def suggest(titre_candidat):
    "Suggests a title from the airs_ref document for an air found in the tesseract"
    with open(airs_ref, "r", encoding="utf8") as f:
        airs_refs = [ line.rstrip() for line in f ]
    best_candidate_fuzzy = process.extractOne(titre_candidat, airs_refs)
    best_candidate_difflib = difflib.get_close_matches(titre_candidat, airs_refs, n=1, cutoff=0.7)
    if best_candidate_fuzzy[1] >= 90 :
        best_candidate = best_candidate_fuzzy[0] 
    else :
        best_candidate = best_candidate_difflib
    return best_candidate


if __name__ == '__main__':
    #args = parser.parse_args()
    #id = args.id_work
    #extract(id)
    id1 = "91"
    #character_list_regex.dramatis_personae(id1)
    extract(id1)

    