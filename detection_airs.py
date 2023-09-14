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

import argparse
import glob 
import os.path

import re 
from fuzzywuzzy import process
import difflib
from difflib import SequenceMatcher
from bs4 import BeautifulSoup

from config import dossier
from config import airs_ref
from config import dossier_out
import character_list_regex
import encoding

parser = argparse.ArgumentParser()
parser.add_argument("id_work", action='store',
                    help="gives candidates in id_work provided and writes them in new doc >  input ';' to reject the line, anything else to add it")
parser.add_argument("--mode", "-m", choices=['extract', 'eval', 'auto'], default="extract",
                    help="extract : writes the id_work_airs.csv, default mode. Add options 'characters'and 'sem_search' for full implementation\
                        eval : evaluates the results on evaluation corpus\
                        auto : automatically extracts. 'all' in place of the id_work extracts the entire directory in config.py")
parser.add_argument("--encode", "-e", action="store_true",
                help="optional output of the encoding of the stage element")
parser.add_argument("--characters", "-c", action="store_true",
                help="add the character list in the output and fine tunes the title search")
parser.add_argument("--sem_search", "-s", action="store_true",
                help="add the semantic search to the suggested titles")
parser.add_argument("--total", "-t", action="store_true",
                help="prints the macrostats in evaluation mode.")


#list of regular expressions searched in the play
AIR_extended = re.compile(r"^(^|\W*)\b(?<!'\| )([AâÂÀĀāǍǎĂăÃãáÅåÄäĄÆÁà][IiïîÎİɪɩĪīǏǐĬĭÍíÎîĨĩÌìÏỊıJɭĺĹĿŁŀłtTLlrwmns1u][rRŔʀŕŘřɼɽſßŖbB8nNtsaAEpe])\W*\b ?:?\W*")
CHOEUR = re.compile(r"^(^|\W)\b(?<!\|' )\b[Cc][Hh][OʚɞŌōǑǒÓÔóôÒòÖöŎŏØøɸÕõʠŐőʘɵɶɷŒœ][EÉÈÊĚĒĔĖĘɛéèê]?[UuŪūǓǔŬŭÚúÛûŨũÙùÜüűŰǕǖǛǜǗǘŮůʋǙǚŲųʊ][Rr]\b\W*")
REPRISE = re.compile(r"^(^|\W)\b(?<!\|' )\b[R][EÉÈÊéèê][PRF][IiïîÎİɪɩĪīǏǐĬĭÍíÎîĨĩÌìÏİıJɭĺĹĿŁŀłtTLl1][Ss][EÉÈÊéèê]\b.*")
COUPLET = re.compile(r"^(^|\W)\b(?<!' )\b[Cc][Oo][Uu][Pp][IiïLltwmns1]?[Ee][IiïîÎİɪɩĪīǏǐĬĭÍíÎîĨĩÌìÏİıJɭĺĹĿŁŀłtTLl1][S5]?\W*")
FINALE = re.compile(r"^(^|\W)\b(?<!' )\b[FE][IiïLltwmns1][NMR][AâÂÀáÁà][LlIiíÍïÏ][EÉÈÊéèê]?\W*")
DUO = re.compile(r"^(^|\W)\b(?<!' )\bDUO \W?.*")
TRIO = re.compile(r"^(^|\W)\b(?<!' )\bTRIO \W?.*")
regex_filtra = [AIR_extended, CHOEUR, REPRISE, COUPLET, FINALE, DUO, TRIO]


#######################################################MODE EXTRACTION#################################################################

def extract(id_work):
    """Produces a list containing idWork;idAir;ocrAir;ocrLine;suggestedTitle;isair
    written in a idWork_airs.txt doc in corresponding directory"""
    #for evaluation mode only > select the txt file in the directory if not tesseract:
    #docs_txt = [file for file in glob.glob(f"{dossier_id}/*.txt") if os.path.basename(file).endswith("tesseract.txt")]
    doc_entree = f"{dossier}/{id_work}/{id_work}_03_all-text_tesseract.txt"
    if not os.path.exists(doc_entree):
        print("***tesseract inexistant, identification des airs depuis l'OCR original***\n")
        doc_entree = f"{dossier}/{id_work}/{id_work}_00_all-text_original-ocr.txt"
    with open(doc_entree, "r", encoding="utf8") as f:
        res = []
        count_line = 0
        count_air = 0
        for line in f:
            count_line += 1
            l = line.rstrip()                
            #looking for a match between one of the regex above and the line:
            for r1 in regex_filtra:
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
    #possibility to restart the selection process:
    verif(id_work)     
    ecriture(id_work, res)
            
def isair(chaine, ligne):
    """
    Vérification manuelle par l'utilisateur du contenu de la chaine extraite par la regex
    le numéro de ligne a pour but d'aider à identifier les airs
    input [n] pour non
    """
    yn = input(f'''{chaine}:{ligne}:      ''')
    if yn == ';':
        return chaine, "0"
    else:
        return chaine, "1"

def cherche_titre(chaine, id_work):
    """
    Dans les cas où l'air n'a pas de titre (i.e. "AIR :" ou "CHOEUR."), détermine la prochaine ligne capable d'être un titre. 
    Exclusion d'une ligne vide, d'une didascalie ou d'un nom de personnage
    """
    if args.characters:
        with open(f"{dossier}/{id_work}/05_tune_names/{id_work}_characters.txt", "r", encoding="utf8") as f:
            character_list = [ line.rstrip() for line in f ]
            for c in character_list:
                if re.search(c, chaine):
                    return False
    #exclusion des lignes vides
    if re.fullmatch(r"(\n|\s+)", chaine):
        return False
    #exclusion des didascalies
    if re.search(r"^(^| )[\{\(].*[\}\)]?", chaine):
        return False
    else:
        return True

def suggest(titre_candidat):
    "Suggests a title from the airs_ref document for an air found with extract()"
    with open(airs_ref, "r", encoding="utf8") as f:
        airs_refs = [ line.rstrip() for line in f ]
    best_candidate_fuzzy = process.extractOne(titre_candidat, airs_refs)
    best_candidate_difflib = difflib.get_close_matches(titre_candidat, airs_refs, n=1, cutoff=0.7)
    print(f"Candidat: {titre_candidat}\n\t[1]String matching fuzzy :{best_candidate_fuzzy}")
    if best_candidate_difflib:
        ratio_difflib = round(SequenceMatcher(None, best_candidate_difflib[0], titre_candidat).ratio()*100, 2)
        print(f"\t[2]String matching difflib :({best_candidate_difflib[0]}, {ratio_difflib})")
    if args.sem_search:
        best_candidate_semsearch = semantic_search.search_simple(titre_candidat)
        print(f"\t[3]Semantic search :{best_candidate_semsearch[0]}")
        ratio_sem = best_candidate_semsearch[0][1]
    print("\t[;]Autre\n")
    answer = input("Selectionnez option :\t")
    while answer not in '123;' or answer == '':
        answer = input("Selectionnez option :\t")
    if answer == '1':
        return best_candidate_fuzzy[0]
    if answer == '2' and best_candidate_difflib:
        return best_candidate_difflib[0]
    if answer == '3' and args.sem_search:
        return best_candidate_semsearch[0][0]
    if answer == "3" and not args.sem_search:
        answer = ";"
    if answer == ';' or (answer == '2' and not best_candidate_difflib):
        print("*******Meilleurs candidats*******")
        for d in process.extract(titre_candidat, airs_refs, limit=3):
            print(d[0])
        print(chr(10).join(difflib.get_close_matches(titre_candidat, airs_refs, n=3)))
        if args.sem_search:
            for candidat in best_candidate_semsearch:
                print(candidat[0])
        manual_input = input("\nEntrez la standardisation manuellement:\n")
        return manual_input


def verif(id):
    """Propose de recommencer le processus de sélection depuis le début en mode extraction."""
    val = input("\nValider les données entrées ? [y]/n\t")
    if val == "n":
        extract(id)

def ecriture(id_work, liste):
    dossier_sortie = f"{dossier}/{id_work}/05_tune_names/"
    if not os.path.exists(dossier_sortie):
        os.makedirs(dossier_sortie)
    if args.mode == 'auto': 
        with open(f"{dossier_sortie}/{str(id_work)}_airs_auto.csv" , "w", encoding="utf8") as g:
            g.write("id_work;idAir;title;line;best-candidate-title;isAir\n")
            for ligne in liste:
                g.write(ligne + "\n")
    else:
        with open(f"{dossier_sortie}/{str(id_work)}_airs.csv" , "w", encoding="utf8") as g:
            g.write("id_work;idAir;title;line;best-candidate-title;isAir\n")
            for ligne in liste:
                g.write(ligne + "\n")

################################################################MODE AUTOMATIC####################################################################################################
def auto(id_work):
    doc_entree = f"{dossier}/{id_work}/{id_work}_03_all-text_tesseract.txt"
    if not os.path.exists(doc_entree):
        print("***tesseract inexistant, identification des airs depuis l'OCR original***\n")
        doc_entree = f"{dossier}/{id_work}/{id_work}_00_all-text_original-ocr.txt"
    with open(doc_entree, "r", encoding="utf8") as f:
            res = []
            count_line = 0
            count_air = 0
            for line in f:
                count_line += 1
                l = line.rstrip()                
                #looking for a match between one of the regex above and the line:
                for r1 in regex_filtra:
                    if r1.search(l):
                        count_air += 1
                        #automatic selection of the candidates : 
                        air = l.strip()           
                        air = re.sub(";", "", str(l.strip()))
                        #fullmatch means the line doesn't have a title, in which case the title will be the 1st line of the song:
                        if r1.fullmatch(str(air)):
                            titre = next(f) 
                            while cherche_titre(titre, id_work) == False:
                                titre = next(f)   
                            titre = re.sub(";", "", str(titre))
                            res.append(str(id_work) + ";" + str(count_air) + ";"+   str(air)+ '=' + str(titre.rstrip()) + ";" + str(count_line)  + ";" + str(select_best(titre.rstrip())) )
                        else:
                            titre = air
                            res.append(str(id_work) + ";" + str(count_air) + ";"+ str(titre) + ';' + str(count_line) + ";" + str(select_best(titre)))
    ecriture(id_work, res)

def select_best(titre_candidat):
    "Selects the best standard title"
    res =[]
    with open(airs_ref, "r", encoding="utf8") as f:
        airs_refs = [ line.rstrip() for line in f ]
    best_candidate_fuzzy = process.extractOne(titre_candidat, airs_refs)
    best_candidate_difflib = difflib.get_close_matches(titre_candidat, airs_refs, n=1, cutoff=0.7)
    if args.sem_search:
        best_candidate_semsearch = semantic_search.search_simple(titre_candidat)
        ratio_sem = best_candidate_semsearch[0][1]
        res.append(round(ratio_sem))
    if best_candidate_difflib:
        ratio_difflib = round(SequenceMatcher(None, best_candidate_difflib[0], titre_candidat).ratio()*100, 2)
    else: ratio_difflib = 0
    if best_candidate_fuzzy:
        ratio_fuzzy = best_candidate_fuzzy[1]
    else: ratio_fuzzy = 0
    res.append(ratio_difflib)
    res.append(ratio_fuzzy)
    if sorted(res, reverse=True)[0] == ratio_difflib:
        return best_candidate_difflib[0]
    if sorted(res, reverse=True)[0] == ratio_fuzzy:
        return best_candidate_fuzzy[0]
    if sorted(res, reverse=True)[0] == ratio_sem:
        return best_candidate_semsearch[0][0]


################################################################MODE EVALUATION####################################################################################################
# seulement après l'extraction
def eval(id_work):
    """
    Mode d'évaluation pour le corpus d'évaluation : comparaison des airs sélectionnés avec les airs annotés manuellement par Lara Nugues.
    """
    #there should only be one xml document in the directory:
    docs_xml = [file for file in glob.glob(f"{dossier}/{id_work}/*.xml")]
    for doc_xml in docs_xml:
        with open(f"{dossier}/{id_work}/05_tune_names/{str(id_work)}_airs.csv" , "r", encoding="utf8") as f,\
            open(f"{doc_xml}", "r", encoding="utf8") as g,\
            open(f"{dossier}/{id_work}/05_tune_names/{str(id_work)}_stats.csv" , "w", encoding="utf8") as h,\
            open(f"{dossier_out}/stats.csv" , "a", encoding="utf8") as i:
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
    with open(f"{dossier_out}/stats.csv" , "r", encoding="utf8") as i:
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
    if args.sem_search:
        import semantic_search
    if args.mode == "extract":
        extract(id)
    #only if annotations_fr-characters.csv is available for the corpus:
    if args.characters:
        character_list_regex.dramatis_personae(id)
    if args.encode:
        encoding.encode_air(id)
    if args.mode == "eval":
        eval(id)
    if args.total:
        print(totaux())
    if args.mode == 'auto':
        if id == 'all':
            files = [file for file in glob.glob(f"{dossier}/*")]
            for file in files:
                cherche_id = re.fullmatch(rf"{dossier}\\(\d+)", file)
                id_corpus = cherche_id.group(1)
                print(f"traitement de {id_corpus}")
                auto(id_corpus)
        else:
            auto(id)


