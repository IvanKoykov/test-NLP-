import pandas as pd
import nltk
import pymorphy2
#import re
#import numpy as np
#from pymorphy2 import MorphAnalyzer
#from nltk.corpus import stopwords
import warnings
warnings.filterwarnings("ignore")
nltk.download('stopwords')


df=pd.read_csv('test_data.csv')


def search_two_part_word(doc):
    doc = doc.lower()
    doc = doc.replace('до свидания', 'до_свидания')
    doc = doc.replace('до завтра', 'до_завтра')
    doc = doc.replace('добрый день', 'добрый_день')
    doc = doc.replace('добрый вечер', 'добрый_вечер')
    doc = doc.replace('доброе утро', 'доброе_утро')
    return doc


def search_name(doc):
    # probability score threshold
    prob_thresh = 0.4
    name = 0
    morph = pymorphy2.MorphAnalyzer()
    for word in nltk.word_tokenize(doc.text):
        # print(word,"  aaaaaaaa")
        for p in morph.parse(word):
            # print(p,"   sssss")
            if 'Name' in p.tag and p.score >= prob_thresh:
                # print('{:<12}\t({:>12})\tscore:\t{:0.3}\t{}'.format(word, p.normal_form, p.score,doc['index']))
                name = word

    return name


def search_greeting_farewell(doc):
    dict_welcome=['здравствуйте','добрый_день']
    dict_goodbye=['до_свидания','пока']
    temp={}
    for token in doc.text.split():
        if token in dict_welcome:
            temp='welcome'
        elif token in dict_goodbye:
            temp='goodbye'
    return temp


if __name__ == "__main__":
    df_for_lematize=df.text
    df_for_lematize = df_for_lematize.apply(search_two_part_word)
    serch_name = df_for_lematize.reset_index().apply(search_name, axis=1)
    greet_farew = df_for_lematize.reset_index().apply(search_greeting_farewell, axis=1)
    df['idx_name'] = serch_name
    df["welcome"] = ""
    df["goodbye"] = ""
    for i, el in enumerate(greet_farew):
        if el == 'welcome':
            df['welcome'][i] = 1
            df['goodbye'][i] = 0
        elif el == "goodbye":
            df['welcome'][i] = 0
            df['goodbye'][i] = 1
        else:
            df['welcome'][i] = 0
            df['goodbye'][i] = 0

    df_only_manager = df[df.role == 'manager']
    final = {}
    for i in df_only_manager.dlg_id.unique():
        temp = {}
        # print( df_only_manager[['text','role']][df_only_manager.dlg_id==i][df_only_manager.welcome!=0])
        # print( df_only_manager[df_only_manager.dlg_id==i][df_only_manager.idx_name!=0])
        try:
            temp['welcome'] = (
            df_only_manager.text[df_only_manager.dlg_id == i][df_only_manager.welcome != 0].values[0])
        except:
            temp['welcome'] = '-'
        try:
            temp['goodbye'] = (
            df_only_manager.text[df_only_manager.dlg_id == i][df_only_manager.goodbye != 0].values[0])
        except:
            temp['goodbye'] = '-'
        try:
            temp['name_phrase'] = (
            df_only_manager.text[df_only_manager.dlg_id == i][df_only_manager.idx_name != 0].values[0])
        except:
            temp['name_phrase'] = '-'
        try:
            temp['name'] = (
            df_only_manager.idx_name[df_only_manager.dlg_id == i][df_only_manager.idx_name != 0].values[0])
        except:
            temp['name'] = '-'

        final[i] = temp
    print(final)


