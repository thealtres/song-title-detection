
from config import dossier
from config import airs_ref
from config import dossier_sortie
from config import suffix_tesseract
from config import suffix_original_ocr
from config import suffix_doc_sortie

from lxml import etree
from lxml.builder import E

import glob 
import os.path

#encodage par concaténation:
def encode_air(id_work):
    """ 
    Ecriture depuis le text brut d'un document xml avec les élément <stage> correspondant aux airs sélectionnés dans le mode extraction.
    """
    doc_entree = f"{dossier}/{id_work}/{id_work}{suffix_tesseract}"
    if not os.path.exists(doc_entree):
        doc_entree = f"{dossier}/{id_work}/{id_work}{suffix_original_ocr}"
    doc_sortie_ecriture = f"{dossier}/{id_work}/{dossier_sortie}/{id_work}_airs-encodes.xml"
    doc_air = f"{dossier}/{id_work}/{dossier_sortie}/{str(id_work)}{suffix_doc_sortie}.csv"
    with open(doc_entree, "r", encoding="utf8") as f1,\
        open(doc_air, "r", encoding="utf-8") as f2,\
        open(doc_sortie_ecriture, "w", encoding="utf-8") as f3:
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
                f3.write(f'''<stage type="tune" id="{line}">{line}</stage>\n\t<l>{line}</l>\n''')
            else:
                f3.write(str(line) + "\n")
        f3.write(''''\n\t</body>\n</text>''')