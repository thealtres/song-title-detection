# Encoding tunes programs 

- identification of couplet titles with detection_airs.py
- character_list_regex.py writes a list of characters for any given id_work from the manual - annotation in annotations_fr-characters.csv
- liste_des_noms_d-airs_standards.txt is used as a reference in the string matching process 

## How to use the program

in config.py change the paths so that it matches your directory
then : 

```python detection_airs.py [id_work]```

with id_work being a play already annotated manually. 

## output

In the directory corpus-items/id_work, the following documents are created :
- id_work_characters.txt : contains the characters (regex)
- id_work_airs.txt : contains idWork;idAir;best-candidate-title;title;line



