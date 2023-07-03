
from config import dossier
from config import airs_ref

from lxml import etree
from lxml.builder import E

import glob 
import os.path

#encodage par concaténation:
def encode_air(id_work):
    """ Ecriture depuis le text brut d'un document xml avec les élément <stage> correspondant aux airs sélectionnés dans le mode extraction.
    """
    dossier_id = f"{dossier}/{id_work}"
    #doc_sortie = f"{dossier_id}/encodage-airs/{id_work}_airs-encodes.xml"
    #doc_air = f"{dossier_id}/{str(id_work)}_airs.csv"
    #for testing purposes:
    doc_air = "01_airs.csv"
    doc_txt = "01_03_all-text_tesseract.txt"
    doc_sortie = f"{id_work}_airs-encodes.xml"
    #docs_txt = [file for file in glob.glob(f"{dossier_id}/*.txt") \
        #if os.path.basename(file).endswith("tesseract.txt")]
    #for doc_entree in docs_txt: 
    with open(doc_txt, "r", encoding="utf8") as f1,\
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

#encodage par construction d'un arbre lxml
def encode(id_work):
    #dossier_id = f"{dossier}/{id_work}"
    #doc_sortie = f"{dossier_id}/{id_work}_airs-encodes.xml"
    #doc_air = f"{dossier_id}/{str(id_work)}_airs.csv"
    #for testing purposes:
    doc_air = "test/01_airs.csv"
    doc_txt = "test/01_03_all-text_tesseract.txt"
    doc_sortie = f"test/{id_work}_airs-encodes.xml"
    #docs_txt = [file for file in glob.glob(f"{dossier_id}/*.txt") \
        #if os.path.basename(file).endswith("tesseract.txt")]
    #for doc_entree in docs_txt: 
    with open(doc_txt, "r", encoding="utf8") as f1,\
        open(doc_air, "r", encoding="utf-8") as f2,\
        open(doc_sortie, "wb") as f3:
        airs = []
        airs_id = []
        for line in f2:
            colonne = line.rstrip().split(";")
            if "=" in colonne[2]:
                airs_id.append(colonne[2].split("=")[1])
            else:
                airs.append(colonne[2])
        poem = etree.Element("poem")
        body = etree.SubElement(poem, "body")
        text_ligne = [line.rstrip() for line in f1]
        body = E("body", [str(l) if l.strip() not in airs else E("stage", str(l)) for l in text_ligne ])
        f3.write(etree.tostring(poem, pretty_print=True, xml_declaration=True))


if __name__ == '__main__':
    idWork = "01"
    encode(idWork)
    #encode_air(idWork)