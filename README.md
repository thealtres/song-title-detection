# Encoding tunes programs 

- identification of couplet titles with detection_airs.py
- character_list_regex.py writes a list of characters for any given id_work from the manual annotation in annotations_fr-characters.csv (not used in evaluation mode)

Data:

- liste_des_noms_d-airs_standards.txt is used as a reference for the program to suggests a title already existing.
- annotations_fr-characters.csv is used to fetch the character names within a play (optional). 

## How to use the program

in config.py change the paths so that it matches your directory
then : 

```python detection_airs.py [id_work] [--mode/-m {extract, eval}] [--sem_search/-s] [--characters/-c] [--encode/-e]default = --mode extract```

with id_work being a unique id for each play with an OCR : looks for the tesseract OCR but will use the original text if a tesseract OCR is not present. Creates a directory ```05_tune_names``` containing ```[id_work]_airs.csv```<br> 
--mode being by default the extraction mode following the next steps: <br>
The program will give a candidate line : input ";" to reject it, any other key will add the line to the list. <br>
Tips: Add lines that do not contain titles such as "AIR :" or "CHOEUR." : in that situation the program will select the next line as the title. This option works better with the option --characters selected as it will discriminate the character names as potential song titles <br>
The program will then suggest titles from a reference document containing well known song titles. By default only string matching suggestions are made. The semantic search option provides a third suggestion. By selecting ";" it is possible to write down the correct title. <br>
A validation after all the lines have been filtered is asked : input "n" to select the candidates again. <br>
Eval mode will write the precision, recall and f1 score in a ```[id_work]_stats.csv``` doc and print the result for those stats for the entire corpus so far in the file ```stats.csv``` in the ```out``` directory.<br>
Sem_Search will implement the semantic search during the selection of a proper title.<br>
Characters is only available for plays that have been annotated manually as it looks for the character names in a seperate document, creates a document called ```[id_work]_characters.txt```. <br>
Encoding will encode in a new xml document the element <stage type="tune"> from the OCR available.

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

- id_work_airs-encodes.xml : same as raw text file with <stage type="tune"> around the identified songs titles.
- id_work_stats.csv :

        - Airs candidats:              
        - Airs manuellement filtrés :                 
        - Airs réelement présents :                
        - Précision:              
        - Rappel:           
        - Mesure-F1:
        - optional Non attrapé : titles missed by the program
        - optional Supplémentaire : titles found by the program but not annotated in the evaluation corpus.

