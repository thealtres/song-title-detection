# basic configurations for the entire module : 
# - detections_airs.py (main program)
# - character_list_regex
# - encoding
# - semantic_search

# *** CONFIGURATIONS 
# dossier : path linking to the corpus in it's entirety
# suffix_tesseract : standardized name of the tesseract OCR for the play
# suffix_original_ocr : standardized name of the original OCR for the play

# dossier_sortie : name of the directory created in each corpus item where the outputs will go
# suffix_doc_sortie : custom name for the output.

# airs_ref : txt document containing the titles of the couplets corrected manually
# characters_sheet : csv containing all the characters annotated manually
# dossier_stats : directory for the evaluation mode outputs (performance statistics)

# nom du dossier où se trouvent les items du corpus:
dossier = "corpus"
# dossier = '../thealtres-ocr/corpus-items'

# suffixes des doc txt des pièces d'où sont extraits les airs:
suffix_tesseract = '_03_all-text_tesseract.txt'
suffix_original_ocr = "_00_all-text_original-ocr.txt"

# chemin du dossier créé en sortie :
dossier_sortie = '05_tune_names'
# nom du document csv en sortie :
suffix_doc_sortie = '_airs'
# chemin intégral en sortie :
# '{dossier}/{id_work}/{dossier_sortie}/{id_work}{suffix_doc_sortie}.csv'
# exemple chemin de sortie : 
#  'corpus-items/001/tune_names/001_airs.csv'

# documents de référence pour les options du programme:
airs_ref = "data/liste_des_noms_d-airs_standards.txt"
characters_sheet = f"data/annotations_fr-characters.csv"
dossier_stats = "out"