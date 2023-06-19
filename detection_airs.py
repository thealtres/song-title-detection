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

from bs4 import BeautifulSoup
import glob 
parser = argparse.ArgumentParser()
parser.add_argument("id_work", 
                    help="gives candidates in id_work provided and writes them in new doc >  input 'n' to reject the line, anything else to add it")
parser.add_argument("--mode", "-m", choices=['extract', 'eval'], default="extract",
                    help="extract writes the id_work_airs.csv, default mode. eval evaluates the results")


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
    #doc_entree = f"{dossier}/{id_work}/{id_work}_03_all-text_tesseract.txt"
    #for test corpus, meant for the evaluation of the program :
    docs_txt = glob.glob(f"{dossier}/{id_work}/*.txt")
    for doc_entree in docs_txt:
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
                            titre = re.sub(";", "", str(titre))
                            if r1.fullmatch(str(titre)):
                                titre = next(f) 
                                while cherche_titre(titre, id_work) == False:
                                    titre = next(f)   
                                titre = re.sub(";", "", str(titre))
                                res.append(str(id_work) + ";" + str(count_air) + ";"+   str(air[0])+ ':' + str(titre.rstrip()) + ";" + str(count_line)  + ";" + str(suggest(titre.rstrip())) + ";" + str(air[1]))
                            else:
                                res.append(str(id_work) + ";" + str(count_air) + ";"+ str(titre) + ';' + str(count_line) + ";" + str(suggest(titre)) + ";" + str(air[1]))
                        else:
                            faux_positif = air[0]
                            faux_positif = re.sub(";", "", str(faux_positif))
                            res.append(str(id_work) + ";;" + str(faux_positif) + ";" + str(count_line) + ";;" + str(air[1]))
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
    #withdrawing the character list for the evaluation of the program on corpus-test:
    #with open(f"{dossier}/{id_work}/{id_work}_characters.txt", "r", encoding="utf8") as f:
        #character_list = [ line.rstrip() for line in f ]
        #for c in character_list:
            #if re.search(c, chaine):
                #return False
    if re.fullmatch(r"(\n|\s+)", chaine):
        return False
    if stage_directions.search(chaine):
        return False
    else:
        return True

def suggest(titre_candidat):
    "Suggests a title from the airs_ref document for an air found with extract()"
    with open(airs_ref, "r", encoding="utf8") as f:
        airs_refs = [ line.rstrip() for line in f ]
    best_candidate_fuzzy = process.extractOne(titre_candidat, airs_refs)
    best_candidate_difflib = difflib.get_close_matches(titre_candidat, airs_refs, n=1, cutoff=0.7)
    if best_candidate_fuzzy[1] >= 90 :
        best_candidate = best_candidate_fuzzy[0] 
    else :
        best_candidate = best_candidate_difflib
    return best_candidate


def eval(id_work):
    docs_xml = glob.glob(f"{dossier}/{id_work}/*.xml")
    for doc_xml in docs_xml:
        with open(f"{dossier}/{str(id_work)}/{str(id_work)}_airs.csv" , "r", encoding="utf8") as f,\
            open(f"{doc_xml}", "r", encoding="utf8") as g,\
            open(f"{dossier}/{str(id_work)}/{str(id_work)}_stats.csv" , "w", encoding="utf8") as h,\
            open(f"stats.csv" , "a", encoding="utf8") as i:
            all = 0
            true_candidates = []
            for line in f:
                l = line.rstrip()
                all += 1
                idWork,idAir,ocrAir,ocrLine,suggestedTitle,airOrNot = l.split(";")
                if airOrNot == "1":
                    true_candidates.append(ocrAir)
            precision = len(true_candidates)/all
            soup = BeautifulSoup(g, 'xml')
            true_airs = soup.find_all("stage", type="tune")
            rappel = len(true_candidates)/len(true_airs)
            f1 = (2 * ((precision*rappel) / (precision+rappel)))
            h.write(f"Airs candidats: {all}\
                \nAirs manuellement filtrés : {len(true_candidates)}\
                \nAirs réelement présents : {len(true_airs)}\
                \nPrécision: {precision:.2f}\
                \nRappel: {rappel:.2f}\
                \nMesure-F1: {f1:.2f}")
            i.write(f"\n{id_work};{precision:.2f};{rappel:.2f};{f1:.2f}")

def totaux():
    with open(f"stats.csv" , "r", encoding="utf8") as i:
        i.readline()
        tot_p  = 0
        tot_r = 0
        tot_f = 0
        line_count = 0
        for line in i:
            line_count +=1
            id,precision,rappel,f1 = line.rstrip().split(";") 
            tot_p += float(precision)
            tot_r += float(rappel)
            tot_f  += float(f1)
        return f"\n******Stats du programme sur le corpus******\
                \nPrécision: {tot_p/line_count:.2f}\
                \nRappel: {tot_r/line_count:.2f}\
                \nMesure-F1: {tot_f/line_count:.2f}"
        
        

if __name__ == '__main__':
    args = parser.parse_args()
    id = args.id_work
    #character_list_regex.dramatis_personae(id)
    if args.mode == "extract":
        extract(id)
    if args.mode == "eval":
        eval(id)
        print(totaux())
    #id1 = "91"
    #extract(id1)

    