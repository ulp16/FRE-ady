# FRE-ady
Updated version of the implementation of the Flesch Reading Ease formula for Adyghe. In addition, it provides implementation for English for comparison purpose. 
Latest changes apply to coefficients and constant.

**USAGE:**
1) Recommended Python version is up to 3.9 (no higher).
For version switch do the following:
```
python3 --version

alias python3=python3.9
```
or just use:
```
python3.9
```

3) Install the following packages:

```
% python3 -m pip install lingcorpora

% python3 -m pip install textstat

% python3 -m pip install pandas

% python3 -m pip install nltk

% python3 -m pip install spacy

% python3 -m pip install prettytable    

```

5) Go to/download the folder _scripts_, from there run the script
   
_For Adyghe:_
```
% python3.9 FRE-ady.py --file filename_ady.txt --lang ady  
```
_For English:_
```
% python3.9 FRE-en.py --file filename_en.txt --lang en
```
#========================================================================#

Adyghe/English files for testing are in /ex folder.

#========================================================================#

Code developed by: Uliana Petrunina, contributors: Pavel Pashentsev, Victoria Pugach

Affiliation: _Center for Language and Brain_, _HSE University_

If you use the FRE-ady, please cite the following paper:

Petrunina U., Zdorova N. 2025. Readability assessment of written Adyghe using a baseline approach. In: Proceedings of the International Conference “Dialogue 2025”, 1-10 pp. [URLPaperDialogue2025](https://dialogue-conf.org/wp-content/uploads/2025/04/PetruninaUZdorovaN.031.pdf) 
