# Encoding tunes programs 

- identification of couplet titles with detection_airs.py
- character_list_regex.py writes a list of characters for any given id_work from the manual annotation in annotations_fr-characters.csv (not used in evaluation mode)
- semantic_search.py allows for the optional semantic search of proper song titles. 
- encoding.py encodes in xml the play with the song titles identified.

Data:

- liste_des_noms_d-airs_standards.txt is used as a reference for the program to suggests a title already existing.
- annotations_fr-characters.csv is used to fetch the character names within a play (optional). 

## How to use the program

in config.py change the paths so that it matches your directory
then : 

```python detection_airs.py [id_work] [--mode/-m {extract, eval}] [--sem_search/-s] [--characters/-c] [--encode/-e]default = --mode extract```

with id_work being a unique id for each play with an OCR : looks for the tesseract OCR but will use the original text if a tesseract OCR is not present. Creates a directory ```05_tune_names``` containing ```[id_work]_airs.csv```<br> 
--mode being by default the extraction mode following the next steps: <br>
The program will give a candidate line with its line number: input ";" to reject it, any other key will add the line to the list. <br>
Tips: Add lines that do not contain titles such as "AIR :" or "CHOEUR." : in that situation the program will select the next line as the title. This option works better with the option --characters selected as it will discriminate the character names as potential song titles <br>
The program will then suggest titles from a reference document containing well known song titles. By default only string matching suggestions are made. The semantic search option provides a third suggestion. By selecting ";" it is possible to write down the correct title. <br>
A validation after all the lines have been filtered is asked : input "n" to select the candidates again. <br>
Eval mode will write the precision, recall and f1 score in a ```[id_work]_stats.csv``` doc and print the result for those stats for the entire corpus so far in the file ```stats.csv``` in the ```out``` directory.<br>
Sem_Search will implement the semantic search during the selection of a proper title.<br>
Characters is only available for plays that have been annotated manually as it looks for the character names in a seperate document, creates a document called ```[id_work]_characters.txt```. <br>
Encoding will encode in a new xml document the element stage type "tune" from the OCR available.

## Output

In the directory corpus/id_work, the following documents are created :
- id_work_characters.txt : contains the characters extracted from the manual annotation (annotations_fr-characters.csv), written as regular expressions.
- id_work_airs.csv : contains the following for each line : id_work;idAir;title;line;best-candidate-title;isAir : 

        - id_work 
        - idAir : incremented for each play 
        - title : title as is in the OCR raw txt
        - line : line number in the txt doc
        - best candidate title : using string matching and/or semantic search gives the best candidate within the reference list in "liste_des_noms_d-airs_standards.txt"
        - isAir : booleen, 1 if the line contains a valid air

- id_work_airs-encodes.xml : same as the OCR text file but with element stage type "tune" encoded.
- id_work_stats.csv :

        - Airs candidats:              
        - Airs manuellement filtrés :                 
        - Airs réelement présents :                
        - Précision:              
        - Rappel:           
        - Mesure-F1:
        - Non attrapé : titles missed by the program
        - Supplémentaire : titles found by the program but not annotated in the evaluation corpus.

## Example

```python detection_airs.py 001 -s -c ```

CHŒUR.:378:
input = ```y```
Titre candidat: Air de M. Marius Boullard.
[1]Sting matching fuzzy: ('Air de M. Boullard.', 95)
[2]String matching difflib: Air de M. Boullard.
[3]Semantic search : Air de M. Boullard.
[;]Autre
input = ```1```
output = ```001;1;CHŒUR.=Air de M. Marius Boullard.;378;Air de M. Boullard.;1```
...
001;14;Air : de M. Marius Boullard.;2855;Air de M. Boullard.;1
CHŒUR.:2863:
input = ```;```
output = ```001;;CHŒUR.2863;;0```
...
"CHŒUR, *":3546:
input = ```y```
Candidat: Air: De la belle Polonaise.
        [1]String matching fuzzy :('AIR : Adieu, je vous fuis, bois charmant.', 86)
        [2]String matching difflib :[]
        [3]Semantic search :AIR : Le beau Lycas.

        [;]Autre

Selectionner option :  ```;```
*******Meilleurs candidats*******
AIR : Adieu, je vous fuis, bois charmant.
AIR : Ah !  ah ! ah ! ah ! c'est désolant.
AIR : Ah ! Mon ami, c'est un rayon d'espoir.
AIR : Ah ! ah ! ah ! ah ! ah ! ah ! ah ! ah !
AIR : Ah ! de plaisir notre âme est enivrée.
AIR : De la Marseillaise.
Air : De la galoppe.
Air de la Nacelle. (de Panseron.)
Air de la Parisienne.
Air de la Parisienne.
AIR : Le beau Lycas.
Air : de la Fiancée.
Air : Ô filii.
AIR : Enfans de Polymnie.
Air : C'est charmant.

C/C le meilleur candidat de la liste ou entrez le nom de l'air manuellement:
input : ```Air: De la belle Polonaise.```
ouput : ```132;12;CHŒUR, *=Air: De la belle Polonaise.;3546;Air: De la belle Polonaise.;1```


(In the second case: CHOEUR. was not selected as a valid candidate as it appears only 8 lines after a song title Air : de M. Marius Boullard.)