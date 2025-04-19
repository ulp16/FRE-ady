#-*- coding: utf-8 -*-
################################
#USAGE:
#python version = no higher than 3.9
# % python FRE-ady.py --help 
# Adyghe % python FRE-ady.py --file filename-ady.txt --lang ady
# English %  python FRE-ady.py --file filename-en.txt --lang en
################################

import textstat
from pathlib import Path
from functions import filSenTok,sentWordCount,flesch_reading_ease
import textstat
import argparse
import pandas as pd
from prettytable import PrettyTable, TableStyle
import faulthandler
faulthandler.enable()

# парсинг аргументов из командной строки
parser = argparse.ArgumentParser(description="Анализ сложности адыгейских и англ текстов")
parser.add_argument("--file", required=True, help="Название файла для анализа")        
parser.add_argument("--lang", required=True, choices=["ady", "en"], help="Язык текста")
args = parser.parse_args()

file = args.file
lang = args.lang

if not Path(file).is_file():
    print(f'Ошибка: файл {file} не найден.')
else:
    if lang == 'ady':
        res = filSenTok(file)
        stat = sentWordCount(res[0], res[1], file)
        sentLenAveragX = stat['sentLenAverag'][0]
        syllCountX = stat['syllCount'][0]
        wordCount = stat['wordCount'][0]
        sentCount = stat['sentCount'][0]
        syllCountAverag = stat['syllAverag'][0]
    else:
        with open(file, encoding='utf-8') as f:
            text = f.read()
        sentCount = textstat.sentence_count(text)
        wordCount = textstat.lexicon_count(text, removepunct=True)
        syllCountX = textstat.syllable_count(text)
        sentLenAveragX = wordCount / sentCount  
        syllCountAverag = syllCountX/wordCount
    FRE = flesch_reading_ease(sentLenAveragX, syllCountX, wordCount, file, lang)    
    table = PrettyTable()
    table.field_names = ["Field", "Value"]
    table.align["Field"] = "l"
    table.align["Value"] = "l"
    table.header = True
    table.add_row(["fileName", Path(file).name])
    table.add_row(["language", "Adyghe" if lang == 'ady' else "English"])
    table.add_divider()
    table.add_row(["FleschScore", round(FRE["FRE-score"][0], 2)])
    table.add_divider()
    table.add_row(["sentenceCount", sentCount])
    table.add_row(["wordCount", wordCount])
    table.add_row(["syllableCount", syllCountX])
    table.add_row(["averageSentenceLength", round(sentLenAveragX,2)])
    table.add_row(["averageSyllableLength", round(syllCountAverag,2)])   
    print("\nOUTPUT", flush=True)
    print("%", flush=True)
    print(table, flush=True)
