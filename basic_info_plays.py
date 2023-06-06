"""fetching basic info from web pages containing plays"""

from bs4 import BeautifulSoup
import re

dossier = f"../corpus-items"
id = 115
wiki = "Wikisource"
google_books = "Google"
#for id in range(112, 146, step=1):
with open(f"{dossier}/{id}/{id}.html", "rb") as f:
    soup = BeautifulSoup(f, 'html.parser')
    #page wikisource
    if re.search(wiki, soup.find("title").get_text()):   
        infos = soup.find_all("div", class_="headertemplate")
        for info in infos:
            title = info.find("div", class_="headertemplate-title").find_next().get_text().strip()
            subtitle = info.find("small").get_text().strip()
            author = info.find("div", class_="headertemplate-author").get_text().strip()
            publisher = info.find("span", itemprop="publisher").find_next().get_text().strip()
            date = info.find("time").get_text().strip()
    

  """   #page google livres
    if re.search(google_books, soup.find("title").get_text()):
        infos = soup.find_all("td", id="bookinfo")
        for info in infos:
            title = info.find("h1", class_="booktitle").get_text()
            subtitle = info.find("span", class_="subtitle").get_text()
            author_section = info.find("div", class_="bookinfo_sectionwrap")
            author = author_section.find_all("a", class_="secondary")
            publisher = author_section("div")[-1].get_text()
            
 """
print(title + subtitle + author + publisher + date)