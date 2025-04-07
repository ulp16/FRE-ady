# FRE-ady
Implementation of the Flesch Reading Ease formula for Adyghe. It also provides implementation for English for comparison purpose.

**USAGE:**
1) Recommended Python version is up to 3.9 (no higher).
For version switch do the following:

python3 --version

alias python3=python3.9

3) Install the following packages:
% python3 -m pip install lingcorpora

% python3 -m pip install textstat

% python3 -m pip install pandas

% python3 -m pip install nltk

% python3 -m pip install spacy

% python3 -m pip install prettytable    


5) Run the script
   
_For Adyghe:_

% python FRE-ady.py --file filename_ady.txt --lang ady  

_For English:_

% python FRE-en.py --file filename_en.txt --lang en

#========================================================================#

Adyghe/English files for testing are in /ex folder.

#========================================================================#

Author: Uliana Petrunina, contributors: Pavel Pashentsev, Victoria Pugach

Affiliation: Center for Language and Brain, HSE University
