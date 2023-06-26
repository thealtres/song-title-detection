""""
Alexia Schneider juin 2023
détection des airs et de leur titre
output: [id_work]_airs.txt dans le dossier id_work du corpus 
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
import glob 
import os.path

import re 
from fuzzywuzzy import process
import difflib
from bs4 import BeautifulSoup

from config import dossier
from config import airs_ref
import character_list_regex

parser = argparse.ArgumentParser()
parser.add_argument("id_work", 
                    help="gives candidates in id_work provided and writes them in new doc >  input 'n' to reject the line, anything else to add it")
parser.add_argument("--mode", "-m", choices=['extract', 'eval'], default="extract",
                    help="extract writes the id_work_airs.csv, default mode. eval evaluates the results")

#list of regular expressions searched in the play
AIR_extended = re.compile(r"^(^|\W*)\b(?<!'\| )([AâÂÀĀāǍǎĂăÃãáÅåÄäĄÆÁà][IiïîÎİɪɩĪīǏǐĬĭÍíÎîĨĩÌìÏỊıJɭĺĹĿŁŀłtTLlrwmns1u][rRŔʀŕŘřɼɽſßŖbB8nNtsaAEpe])\W*\b ?:?")
CHOEUR = re.compile(r"^(^|\W)\b(?<!\|' )\b[Cc][Hh][OʚɞŌōǑǒÓÔóôÒòÖöŎŏØøɸÕõʠŐőʘɵɶɷŒœ][EÉÈÊĚĒĔĖĘɛéèê]?[UuŪūǓǔŬŭÚúÛûŨũÙùÜüűŰǕǖǛǜǗǘŮůʋǙǚŲųʊ][Rr]\b\W*")
REPRISE = re.compile(r"^(^|\W)\b(?<!\|' )\b[R][EÉÈÊéèê][PRF][IiïîÎİɪɩĪīǏǐĬĭÍíÎîĨĩÌìÏİıJɭĺĹĿŁŀłtTLl1][Ss][EÉÈÊéèê]\b.*")
COUPLET = re.compile(r"^(^|\W)\b(?<!' )\b[Cc][Oo][Uu][Pp][IiïLltwmns1]?[Ee][TtlLIiï]\W?\b")
FINALE = re.compile(r"^(^|\W)\b(?<!' )\b[FE][IiïLltwmns1][NMR][AâÂÀáÁà][LlIiíÍïÏ][EÉÈÊéèê]?\W?\b")
DUO = re.compile(r"^(^|\W)\b(?<!' )\bDUO \W?.*")
TRIO = re.compile(r"^(^|\W)\b(?<!' )\bTRIO \W?.*")
regex_filtra1 = [AIR_extended, CHOEUR, REPRISE, COUPLET, FINALE, DUO, TRIO]

#regex for the stage direction. Needed for the exclusion of the first line in cherche_titre()
stage_directions = re.compile(r"^(^| )[\{\(].*[\}\)]?")

#default mode : extraction of Air in the play. They will be written in id_work_airs.csv. Encoding of the element <stage type="tune">. 
def extract(id_work):
    """Produces a list containing idWork;idAir;ocrAir;ocrLine;suggestedTitle;isair
    written in a idWork_airs.txt doc in corresponding directory"""
    dossier_id = f"{dossier}/{id_work}"
    #select the txt file in the directory:
    docs_txt = [file for file in glob.glob(f"{dossier_id}/*.txt") \
        if not os.path.basename(file).endswith("_characters.txt") and not os.path.basename(file).endswith("_00_all-text_original-ocr.txt") and not os.path.basename(file).endswith("_00_all-text_original-ocr_no-layout.txt")]
    for doc_entree in docs_txt:
        with open(doc_entree, "r", encoding="utf8") as f:
            res = []
            count_line = 0
            count_air = 0
            for line in f:
                count_line += 1
                l = line.rstrip()                
                #looking for a match between one of the regex above and the line:
                for r1 in regex_filtra1:
                    if r1.search(l):
                        #manual selection of the candidates :    
                        air = isair(l.strip(), count_line)
                        if air[1] == "1": 
                            count_air += 1 
                            titre = air[0]
                            titre = re.sub(";", "", str(titre))
                            #fullmatch means the line doesn't have a title, in which case the title will be the 1st line of the song:
                            if r1.fullmatch(str(titre)):
                                titre = next(f) 
                                while cherche_titre(titre, id_work) == False:
                                    titre = next(f)   
                                titre = re.sub(";", "", str(titre))
                                res.append(str(id_work) + ";" + str(count_air) + ";"+   str(air[0])+ '=' + str(titre.rstrip()) + ";" + str(count_line)  + ";" + str(suggest(titre.rstrip())) + ";" + str(air[1]))
                            else:
                                res.append(str(id_work) + ";" + str(count_air) + ";"+ str(titre) + ';' + str(count_line) + ";" + str(suggest(titre)) + ";" + str(air[1]))
                        else:
                            faux_positif = air[0]
                            faux_positif = re.sub(";", "", str(faux_positif))
                            res.append(str(id_work) + ";;" + str(faux_positif) + ";" + str(count_line) + ";;" + str(air[1]))
    #the result is written in file id_work_airs.csv:
    with open(f"{dossier_id}/{str(id_work)}_airs.csv" , "w", encoding="utf8") as g:
        for ligne in res:
            g.write(ligne + "\n")
    #encoding of the element <stage type="tune"> from the selected candidates.
    encode_air(id_work)
    #possibility to restart the selection process:
    verif(id_work)       
            
def isair(chaine, ligne):
    """
    Vérification manuelle par l'utilisateur du contenu de la chaine extraite par la regex
    le numéro de ligne a pour but d'aider à identifier les airs
    input [n] pour non
    """
    yn = input(f'''"{chaine}":{ligne}:      ''')
    if yn == ';':
        return chaine, "0"
    else:
        return chaine, "1"

def cherche_titre(chaine, id_work):
    """
    Dans les cas où l'air n'a pas de titre (i.e. "AIR :" ou "CHOEUR."), détermine la prochaine ligne capable d'être un titre. 
    Exclusion d'une ligne vide, d'une didascalie ou d'un nom de personnage
    """
    #withdrawing the character list for the evaluation of the program on corpus-test:
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

def verif(id):
    """Propose de recommencer le processus de sélection depuis le début en mode extraction en cas de mauvaise entrée."""
    val = input("\nValider les données entrées ? [y]/n\t")
    if val == "n":
        extract(id)


def encode_air(id_work):
    """ Ecriture depuis le text brut d'un document xml avec les élément <stage> correspondant aux airs sélectionnés dans le mode extraction.
    """
    dossier_id = f"{dossier}/{id_work}"
    doc_sortie = f"{dossier_id}/{id_work}_airs-encodes.xml"
    doc_air = f"{dossier_id}/{str(id_work)}_airs.csv"
    docs_txt = [file for file in glob.glob(f"{dossier_id}/*.txt") \
        if not os.path.basename(file).endswith("_characters.txt") and not os.path.basename(file).endswith("_00_all-text_original-ocr.txt") and not os.path.basename(file).endswith("_00_all-text_original-ocr_no-layout.txt")]
    for doc_entree in docs_txt: 
        with open(doc_entree, "r", encoding="utf8") as f1,\
            open(doc_air, "r", encoding="utf-8") as f2,\
            open(doc_sortie, "w", encoding="utf-8") as f3:
            airs = []
            airs_id = []
            for line in f2:
                colonne = line.rstrip().split(";")
                if "=" in colonne[2]:
                    airs_id.append(colonne[2].split("=")[1])
                else:
                    airs.append(colonne[2])
            f3.write(f'''<?xml version='1.0' encoding='UTF-8'?>''')
            f3.write('''\n<text>\n\t<body>\n''')
            for line in f1:
                line = line.rstrip()
                if line in airs:
                    f3.write(f'''<stage type="tune">{line}</stage>\n''')
                elif line in airs_id:
                    f3.write(f'''<stage type="tune" id="{line}"></stage>\n\t<l>{line}</l>\n''')
                else:
                    f3.write(str(line) + "\n")
            f3.write(''''\n\t</body>\n</text>''')


def eval(id_work):
    """
    Mode d'évaluation pour le corpus d'évaluation : comparaison des airs sélectionnés avec les airs annotés manuellement par Lara Nugues.
    """
    dossier_id = f"{dossier}/{id_work}"
    docs_xml = [file for file in glob.glob(f"{dossier_id}/*.xml") \
        if not os.path.basename(file).endswith("_airs-encodes.xml")]
    for doc_xml in docs_xml:
        with open(f"{dossier_id}/{str(id_work)}_airs.csv" , "r", encoding="utf8") as f,\
            open(f"{doc_xml}", "r", encoding="utf8") as g,\
            open(f"{dossier_id}/{str(id_work)}_stats.csv" , "w", encoding="utf8") as h,\
            open(f"stats.csv" , "a", encoding="utf8") as i:
            all = 0
            true_candidates = []
            for line in f:
                l = line.rstrip()
                all += 1
                idWork,idAir,ocrAir,ocrLine,suggestedTitle,airOrNot = l.split(";")
                if airOrNot == "1":
                    if "=" in ocrAir:
                        true_candidates.append(ocrAir.split("=")[1])
                    else:
                        true_candidates.append(ocrAir)           
            precision = len(true_candidates)/all
            soup = BeautifulSoup(g, 'xml')
            true_airs = [t.get_text() for t in soup.find_all("stage", type="tune")  ] 
            true_airs_id = [t.get("id") for t in soup.find_all("stage", type="tune") if t.get("id") != None ]    
            rappel = len(true_candidates)/len(true_airs)
            if rappel > 1.00:
                rappel = 1.00
            f1 = (2 * ((precision*rappel) / (precision+rappel)))
            h.write(f"Airs candidats: {all}\
                \nAirs manuellement filtrés : {len(true_candidates)}\
                \nAirs réelement présents : {len(true_airs)}\
                \nPrécision: {precision:.2f}\
                \nRappel: {rappel:.2f}\
                \nMesure-F1: {f1:.2f}")
            airs_supplementaires = []
            airs_valides = [process.extractOne(candidat, true_airs)[0]  if process.extractOne(candidat, true_airs)[1] >= 90 or candidat in true_airs_id else airs_supplementaires.append(candidat) for candidat in true_candidates]            
            for air in true_airs:
                if air not in airs_valides:
                    print("Non attrapé:" + air)
                    h.write(f"\nNon attrapé: {air}")
            for air in airs_supplementaires:
                print("Supplémentaire:" + air)
                h.write(f"\nSupplémentaire: {air}")
            i.write(f"\n{id_work};{precision:.2f};{rappel:.2f};{f1:.2f}")
            h.write(f"\n\n***Airs du xml***:\n" + chr(10).join(true_airs) + chr(10).join(true_airs_id) )
            h.write(f"\n\n***Airs identifiés dans le txt***:\n" + chr(10).join(true_candidates))
            h.write(f"\n\n***Airs du txt validés dans le xml***:\n")
            for a in airs_valides:
                if a != None:
                    h.write(a + "\n")
                            
def totaux():
    """Affichage des macros du programme en mode évaluation. """
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
        return f"\n******Macrostats du programme sur le corpus d'évaluation******\
                \nPrécision: {tot_p/line_count:.2f}\
                \nRappel: {tot_r/line_count:.2f}\
                \nMesure-F1: {tot_f/line_count:.2f}"
        
if __name__ == '__main__':
    args = parser.parse_args()
    id = args.id_work
    if args.mode == "extract":
        character_list_regex.dramatis_personae(id)
        #extract(id)
    if args.mode == "eval":
        eval(id)
        #print(totaux())
