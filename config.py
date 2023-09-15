# basic configurations for the entire module : 
# - detections_airs.py (main program)
# - character_list_regex
# - encoding
# - semantic_search

# *** CONFIGURATIONS 
#     dossier : path linking to the corpus in it's entirety
#     airs_ref : path linking to the document containing the titles of the couplets corrected manually
#     suffix_dossier : name of the directory created where the outputs will go (not a path)
#     characters_sheet : path linking to the csv containing all the characters annotated manually
#     dossier_stats : directory for the evaluation mode outputs (performance statistics)


# dossier = '../thealtres-ocr/corpus-items'
dossier = "corpus"
suffix_dossier = '05_tune_names'
airs_ref = "data/liste_des_noms_d-airs_standards.txt"
characters_sheet = f"data/annotations_fr-characters.csv"
dossier_stats = "out"