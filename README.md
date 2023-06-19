# Encoding tunes programs 

- identification of couplet titles with detection_airs.py
- character_list_regex.py writes a list of characters for any given id_work from the manual annotation in annotations_fr-characters.csv (not used in evaluation mode)
- liste_des_noms_d-airs_standards.txt is used as a reference in the string matching process 

## How to use the program

in config.py change the paths so that it matches your directory
then : 

```python detection_airs.py [id_work] [--mode/-m {extract, eval}]```

with id_work being a play already annotated manually. <br> 
and mode being by default the extraction mode following the next steps: <br>
The program will give a candidate line : input "n" to reject it, any other key will add the line to the list. <br>
Add lines that do not contain titles such as "AIR :" or "COUPLET." : in that situation the program will select the next line as the title. <br>
Eval mode will write the precision, recall and f1 score in a [id_work]_stats.csv doc and print the result for those stats for the entire corpus so far. 

## output

In the directory corpus/id_work, the following documents are created :
- id_work_characters.txt : contains the characters (regex)
- id_work_airs.txt : contains the following for each line : id_work;idAir;title;line;best-candidate-title;isAir
        -- id_work 
        -- idAir : incremented for each play 
        -- title : title as is in the OCR raw txt
        -- line : line number in the txt doc
        -- best candidate title : using string matching, gives the best candidate within the reference list in "liste_des_noms_d-airs_standards"
        -- isAir : booleen, 1 if the line contains a valid air



