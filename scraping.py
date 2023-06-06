"""scraping and downloading pages """

"""lang	workId	title	year	decade	authors	genre	source	method	pdf	toOrder	url	playList	importance	notes	ocrDone"""

import requests
from bs4 import BeautifulSoup
import os
import time

with open("pieces_supplementaires.txt", "r", encoding="utf8") as f1:
    liens = [line.rstrip() for line in f1 ]
id_work = 111
for lien in liens:
    time.sleep(2)
    try:
        page = requests.get(lien)
    except requests.exceptions.RequestException as err:
        print(err)
    else:
        soup = BeautifulSoup(page.text, "html.parser")
        id_work += 1
        dossier_sortie = f"../corpus-items/{id_work}"
        if not os.path.exists(dossier_sortie):
            os.makedirs(dossier_sortie)
        with open(f"{dossier_sortie}/{id_work}.html", "wb") as f:
            f.write(soup.prettify('utf-8'))
            
    
