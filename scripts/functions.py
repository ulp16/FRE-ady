# -*- coding: utf-8 -*-
##########################################
# functions.py — модуль для обработки текста
# Обрабатывает как адыгейский, так и английский текст
##########################################

import textstat
import os
import re
from string import punctuation
from pathlib import Path
import pandas as pd
from spacy.lang.ru import Russian

# Делит файл на части размером не более max_chars символов
def split_file_by_size(file_path, max_chars=1_000_000):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    if len(text) <= max_chars:
        return [file_path]

    parts = []
    start = 0
    part_num = 1

    while start < len(text):
        end = min(start + max_chars, len(text))

        # Ищем точку или перевод строки ближе к концу
        for sep in ['\n', '.']:
            alt_end = text.rfind(sep, start, end)
            if alt_end != -1:
                end = alt_end + 1
                break

        part_text = text[start:end]
        part_filename = f'part{part_num}.txt'
        with open(part_filename, 'w', encoding='utf-8') as pf:
            pf.write(part_text)
        parts.append(part_filename)

        start = end
        part_num += 1

    return parts

# Читает файл, разбитый на части, и возвращает список предложений и токенов
def filSenTok(name):
    parts = split_file_by_size(name)
    lstS = []
    lstT = []
    nlp = Russian()
    nlp.add_pipe('sentencizer')

    for part in parts:
        with open(part, encoding="utf-8") as a:
            text = a.read()
        doc = nlp(text)
        sent = [str(sent).strip() for sent in doc.sents]
        tokens = [el for token in sent for el in re.sub(f"[{re.escape(punctuation)}]", "", token).split()]
        lstS.extend(sent)
        lstT.extend(tokens)

    # Удаление временных файлов
    for part in parts:
        if part != name and os.path.exists(part):
            os.remove(part)

    return (name, lstS, lstT)

# Разделение на слоги для адыгейского языка
def syllAdy(lst):
    with open('o.txt', encoding="utf-8") as o, open('v.txt', encoding="utf-8") as v, open('s.txt', encoding="utf-8") as s:
        lst_o = o.read().splitlines()
        lst_v = v.read().splitlines()
        lst_s = s.read().splitlines()

    new_lst = []
    for el in lst:
        el = el.lower().replace('ӏ', 'Ӏ').replace('i', 'Ӏ')
        new_lst.append(el)

    a = {}
    for el in lst_o:
        key = "o1" if len(el) > 1 else "o"
        a.setdefault(key, []).append(el)
    for el in lst_s:
        a.setdefault("s", []).append(el)
    for el in lst_v:
        a.setdefault("v", []).append(el)

    updated_list = new_lst.copy()
    for key in ["o1", "o", "s", "v"]:
        tmp = []
        for item in updated_list:
            for el in a.get(key, []):
                repl = "0" if key.startswith("o") else ("S" if key == "s" else "V")
                item = item.replace(el, repl)
                if key == "v":
                    item = item.replace("VV", "V").replace("V̆V", "V")
            tmp.append(item)
        updated_list = tmp

    fin = []
    for word, item in zip(new_lst, updated_list):
        count = item.count("V")
        fin.append((word, item, count))

    df = pd.DataFrame(fin, columns=['token', 'syll', '#'])
    return (df['#'].sum(), df['#'].mean(), df)

# Подсчёт статистик по предложениям и слогам
def sentWordCount(file_text, sent_list, file_name):
    features = []
    for el in sent_list:
        word_count = textstat.lexicon_count(str(el), removepunct=True)
        features.append((str(el), word_count))

    df_words = pd.DataFrame(features, columns=['sent', '#'])

    wordCount = sum(df_words['#'])
    sentCount = len(df_words)
    sentLenAverag = df_words['#'].mean()

    tokens = filSenTok(file_name)[2]
    syllc, syllca, _ = syllAdy(tokens)

    t = [[
        'ady', 'lingcorpora', file_name, sentCount, sentCount - 1,
        wordCount, sentLenAverag, syllc, syllca
    ]]
    stat = pd.DataFrame(t, columns=[
        'lang', 'corpus', 'fileName', 'sentCount', 'sentCountAverag',
        'wordCount', 'sentLenAverag', 'syllCount', 'syllAverag'
    ])
    return stat

# Коэффициенты пересчёта для Flesch Reading Ease
def coefficients(sentLenAveragX, sentLenAveragEN, syllAveragX, syllAveragEN):
    coeffASL_X = sentLenAveragEN / sentLenAveragX
    coeffASW_X = syllAveragEN / syllAveragX
    return (coeffASL_X, coeffASW_X)

# Расчёт индекса читаемости
def flesch_reading_ease(sentLenAveragX, syllCountX, wordCountX, name, lang):
    if lang == "ady":
        ASL_X = sentLenAveragX
        ASW_X = syllCountX / wordCountX
        coeffASL_ADY = 1.299342
        coeffASW_ADY = 0.861545
        fre_score = 150.835 - (1.015 * coeffASL_ADY * ASL_X) - (84.6 * coeffASW_ADY * ASW_X)
        t = [['ady', name, fre_score]]
    else:
        ASL_EN = sentLenAveragX
        ASW_EN = syllCountX / wordCountX
        fre_score = 206.835 - (1.015 * ASL_EN) - (84.6 * ASW_EN)
        t = [['en', name, fre_score]]

    return pd.DataFrame(t, columns=['lang', 'fileName', 'FRE-score'])
