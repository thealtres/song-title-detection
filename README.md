# Encoding tunes programs 

- identification of couplet titles with detection_airs.py
- character_list_regex.py writes a list of characters for any given id_work from the manual annotation in annotations_fr-characters.csv
- liste_des_noms_d-airs_standards.txt is used as a reference in the string matching process 

## How to use the program

in config.py change the paths so that it matches your directory
then : 

```python detection_airs.py [id_work]```

with id_work being a play already annotated manually. <br> 
The program will then give a candidate line : input "n" to reject it, any other key will add the line to the list. <br>
Add lines that do not contain titles such as "AIR :" or "COUPLET." : in that situation the program will select the next line as the title. 

## output

In the directory corpus-items/id_work, the following documents are created :
- id_work_characters.txt : contains the characters (regex)
- id_work_airs.txt : contains the following for each line : id_work;idAir;best-candidate-title;title;line
        -- id_work 
        -- idAir : incremented for each play 
        -- best candidate title : using string matching, gives the best candidate within the reference list in "liste_des_noms_d-airs_standards"
        -- title : title as is in the OCR raw txt
        -- line : line number in the txt doc



