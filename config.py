"""basic configurations for the following programs :
- detections_airs
- character_list_regex
- encoding

*** CONFIGURATIONS 
    dossier : path linking to the corpus in it's entirety
    airs_ref : path linking to the document containing the titles of the couplets corrected manually
    characters_sheet : path linking to the csv containing all the characters annotated manually
    """
# corpus habituel :
# dossier = ../thealtres-ocr/corpus-items
dossier = "corpus-evaluation"
airs_ref = "data/liste_des_noms_d-airs_standards.txt"
characters_sheet = f"data/annotations_fr-characters.csv"
dossier_out = "out"