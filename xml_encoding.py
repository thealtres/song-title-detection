import re
from lxml import etree
from bs4 import BeautifulSoup

import glob
import os
from os import listdir
from os.path import isfile, join

import config
from config import dossier
import detection_airs as detect_airs
import character_list_regex as character_list


bbox_pattern = re.compile(r"bbox (\d+) .*")
stage_directions = re.compile(r"[{\(].*[}\)]")
bis = re.compile(r"(\((bis|ters?\W?)\))")


def encode(html, airs, characters, xml):
    """Encodage en xml des airs relevés grace a detection_airs.py
    extraction des lignes depuis l'hocr
    le bbox_pattern sert à relever la position de la ligne où se trouve le titre de l'air
    puis sélection de toutes les lignes au même niveau que la suivante (on suppose la 1e ligne de la chanson)"""
    with open(html, 'r', encoding='utf8') as f,\
        open(airs, "r", encoding="utf8") as g,\
        open(xml, "w+b") as h,\
        open(characters, "r", encoding="utf8") as i:
        soup = BeautifulSoup(f, 'html.parser')
        lines = soup.find_all("span", class_="ocr_line")
        air = [colonne[3] for colonne in [ line.rstrip().split(';') for line in g] ]
        pers = [line.rstrip().strip().upper() for line in i]
        for l in lines:
            if l.get_text().strip() in air:
                poem = etree.Element("div", type="poem")
                lg = etree.SubElement(poem, "lg")  
                stage_tune = etree.SubElement(lg, "stage", type='tune')
                stage_tune.text = l.get_text().strip()
                bbox_air = re.match(bbox_pattern, str(l.get("title")))
                bbox_air = int(bbox_air.group(1))
                bbox_next_line = re.match(bbox_pattern, str(l.find_next("span", class_="ocr_line").get("title")))
                bbox_next_line = int(bbox_next_line.group(1))
                suite = l.find_all_next("span", class_="ocr_line")
                for s in suite:
                    bbox_s = re.match(bbox_pattern, str(s.get("title")))
                    bbox_s = int(bbox_s.group(1))
                    if (bbox_next_line - 70) <= bbox_s <= (bbox_next_line + 100):
                        line = etree.SubElement(lg, "l")
                        line.text = s.get_text().strip()
                        for p in pers:
                            if re.search(p, str(s.get_text().strip())):
                                speaker = etree.SubElement(lg, 'speaker')
                                speaker.text = s.get_text().strip()
                                doublon = speaker.getprevious()
                                lg.remove(doublon)
                        #ajout des balises stage pour les didascalies
                        if re.search(stage_directions, line.text):
                            stage_dir = etree.SubElement(line, "stage")
                            text = re.search(stage_directions, line.text)
                            stage_dir.text = text.group(0) 
                            #line.remove(stage_dir.text) 
                            line.text = re.sub("()", '', line.text)     
                     #else:
                        #bad = etree.SubElement(lg, "bad")
                        #bad.text = s.get_text().strip()
                                        
                h.write(etree.tostring(poem, encoding='utf-8', pretty_print=True))



def extraction_dossier(id_work):
    dossier_hocr_id = f"{dossier}/{id_work}/04_hocr_from_jpg"
    dossier_sortie = f"{dossier}/{id_work}/airs_xml"
    doc_airs = f"{dossier}/{id_work}/{id_work}_airs.txt"
    doc_characters = f"{dossier}/{id_work}/{id_work}_characters.txt"
    try:
        open(doc_airs, "r")
    except FileNotFoundError as err : print(err)
    else:
        if not os.path.exists(dossier_sortie):
            os.makedirs(dossier_sortie)
        docs_html = [d for d in listdir(dossier_hocr_id) if isfile(join(dossier_hocr_id, d))]
        for doc in docs_html:
            doc_html = f"{dossier_hocr_id}/{doc}"
            doc_sortie = f"{dossier_sortie}/{id_work}_airs_{doc[:3]}.xml"
            encode(doc_html, doc_airs, doc_characters, doc_sortie)
        

def nettoyage(id_work):
    "suppression des document xml qui ne contiennent pas d'air"
    dossier_id = f"{dossier}/{id_work}/airs_xml"
    docs = glob.glob(f"{dossier_id}/*.xml")
    for d in docs:
        if os.stat(d).st_size == 0:
            os.remove(d)
if __name__ == '__main__':
    idWork = "102"
    #idWork = input("entrez le nb id")
    #detect_airs.extract(idWork)
    #character_list.dramatis_personae(idWork)
    #config.extraction_dossier(idWork)
    config.nettoyage(idWork)
