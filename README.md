# Automatic detection of song titles in a French corpus

Part of the project Thealtres: https://thealtres.pages.unistra.fr/
<br>Identification of song titles with detection_airs.py : main program with options: 
- character_list_regex.py writes a list of characters for any given id_work from the manual annotation in annotations_fr-characters.csv (not used in evaluation mode).
- semantic_search.py allows for the optional semantic search of proper song titles. 
- encoding.py encodes in xml the play with the song titles identified.

Data:

- liste_des_noms_d-airs_standards.txt is used as a reference for the program to suggests a title already existing.
- annotations_fr-characters.csv is used to fetch the character names within a play. 

## How to use the program

in config.py change the paths so that it matches your directory
then : 

```python detection_airs.py [id_work/'all' (only in mode auto)] [--mode/-m {extract, eval, auto} default = extract] [--sem_search/-s] [--characters/-c] [--encode/-e] [--nb {[int], all} default = 1]```

with id_work being a unique id for each play with an OCR : looks for the tesseract OCR but will use the original text if a tesseract OCR is not present. Creates a directory from the variable ```{dossier_sortie}``` containing as output ```[id_work]{suffix_doc_sortie}.csv```<br> both variable found in config.py to adapt to the corpus used.
--mode being by default the extraction mode following the next steps: <br>
The program will give a candidate line with its line number: input ";" to reject it, any other key will add the line to the list. <br>
Tips: Add lines that do not contain titles such as "AIR :" or "CHOEUR." : in that situation the program will select the next line as the title. This option works better with the option --characters selected as it will discriminate the character names as potential song titles <br>
The program will then suggest titles from a reference document containing well known song titles. By default only string matching suggestions are made. The semantic search option provides a third suggestion. By selecting ";" it is possible to write down the correct title. <br>
A validation after all the lines have been filtered is asked : input "n" to select the candidates again. <br>
Eval mode will write the precision, recall and f1 score in a ```[id_work]_stats.csv``` doc and print the result for those stats for the entire corpus so far in the file ```stats.csv``` in the ```out``` directory.<br>
Sem_Search will implement the semantic search during the selection of a proper title.<br>
Characters is only available for plays that have been annotated manually as it looks for the character names in a seperate document, creates a document called ```[id_work]_characters.txt```. <br>
Encoding will encode in a new xml document the element stage type "tune" from the OCR available.
The automatic mode accepts ```all``` instead of an id number and will then automatically extract all song titles for the entire corpus found in config in the path ```dossier```. 
Automatic mode has one more optional argument ```-nb``` followed by an integer. It adds the number of best standard titles to the output. 

## Output

In the directory corpus/id_work, the following documents are created :
- id_work_characters.txt : contains the characters extracted from the manual annotation (annotations_fr-characters.csv), written as regular expressions.
- id_work_airs.csv : contains the following for each line : id_work;idAir;title;line;best-candidate-title;isAir : 

        - id_work 
        - isAir : booleen, 1 if the line contains a valid air
        - idAir : incremented for each play 
        - title : title as is in the OCR raw txt
        - line : line number in the txt doc
        - best candidate title : using string matching and/or semantic search gives the best candidate within the reference list in "liste_des_noms_d-airs_standards.txt"


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

## Usage in Extract mode (default)

```python detection_airs.py 001 -s -c ```
<br>
__CHŒUR.:378:__<br>
input = ```y```<br>
Titre candidat: Air de M. Marius Boullard.<br>
[1]Sting matching fuzzy: ('Air de M. Boullard.', 95)<br>
[2]String matching difflib: Air de M. Boullard.<br>
[3]Semantic search : Air de M. Boullard.<br>
[;]Autre<br>
input = ```1```<br>
output = ```001;1;CHŒUR.=Air de M. Marius Boullard.;378;Air de M. Boullard.;1```<br>
...<br>
__CHŒUR.:2863:__<br>
input = ```;```<br>
output = ```001;;CHŒUR.2863;;0```<br>
...<br>
__CHŒUR, *__:3546:<br>
input = ```y```<br>
Candidat: Air: De la belle Polonaise.<br>
        [1]String matching fuzzy :('AIR : Adieu, je vous fuis, bois charmant.', 86)<br>
        [2]String matching difflib :[]<br>
        [3]Semantic search :AIR : Le beau Lycas.<br>
        [;]Autre<br>

Selectionner option :  ```;```<br>
*******Meilleurs candidats*******<br>
AIR : Adieu, je vous fuis, bois charmant.<br>
AIR : Ah !  ah ! ah ! ah ! c'est désolant.<br>
AIR : Ah ! Mon ami, c'est un rayon d'espoir.<br>
AIR : Ah ! ah ! ah ! ah ! ah ! ah ! ah ! ah !<br>
AIR : Ah ! de plaisir notre âme est enivrée.<br>
AIR : De la Marseillaise.<br>
Air : De la galoppe.<br>
Air de la Nacelle. (de Panseron.)<br>
Air de la Parisienne.<br>
Air de la Parisienne.<br>
AIR : Le beau Lycas.<br>
Air : de la Fiancée.<br>
Air : Ô filii.<br>
AIR : Enfans de Polymnie.<br>
Air : C'est charmant.<br><br>

C/C le meilleur candidat de la liste ou entrez le nom de l'air manuellement:<br>
input : ```Air: De la belle Polonaise.```<br>
ouput : ```132;1;12;CHŒUR, *=Air: De la belle Polonaise.;3546;Air: De la belle Polonaise.```<br><br>


(In the second case: CHOEUR. was not selected as a valid candidate as it appears only 8 lines after a song title Air : de M. Marius Boullard.)

## Usage in Automatic mode 
```python detection_airs.py -m auto 001 -nb 3 -s -c ```
<br>output(first 3 lines):
<br>>id_work;isAir;idAir;title;line;best-candidate-title;best-candidate-title;best-candidate-title;
>001;1;1;CHŒUR.=Air de M. Marius Boullard.;378;AIR : Adieu, je vous fuis, bois charmant.;Air de M. Boullard.;AIR : Ah !  ah ! ah ! ah ! c'est désolant.
>001;1;2;Air de M. Marius Boullard.;842;AIR : Adieu, je vous fuis, bois charmant.;Air de M. Boullard.;AIR : Ah !  ah ! ah ! ah ! c'est désolant.
<br><br>The options -nb means that the best 3 string matching standard titles are added to the output, -s means that semantic search is activated and -c means that the list of characters is used to exclude a line. 