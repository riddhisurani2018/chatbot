#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import nltk
import re
from nltk.stem import wordnet
from sklearn.feature_extraction.text import CountVectorizer
from nltk import pos_tag
from sklearn.metrics import pairwise_distances
from nltk.corpus import stopwords
import sqlite3

con = sqlite3.connect('/home/riddhi/Desktop/chatbot/chatbot/db.sqlite3')
df = pd.read_sql_query("SELECT * from accounts_text_keyword", con)
df = df.rename(columns={'desc': 'Text Response', 'keyword_value': 'Context'})
df = df.reindex(columns=['Context', 'Text Response'])


def text_normalization(text):
    text = str(text).lower()
    spl_char_text = re.sub(r'[^ a-z]', '', text)
    tokens = nltk.word_tokenize(spl_char_text)
    lema = wordnet.WordNetLemmatizer()
    tags_list = pos_tag(tokens, tagset=None)
    lema_words = []
    for token, pos_token in tags_list:
        if pos_token.startswith('V'):
            pos_val = 'v'
        elif pos_token.startswith('J'):
            pos_val = 'a'
        elif pos_token.startswith('R'):
            pos_val = 'r'
        else:
            pos_val = 'n'
        lema_token = lema.lemmatize(token, pos_val)
        lema_words.append(lema_token)
    return " ".join(lema_words)


text_normalization(df['Context'])
df['lemmatized_text'] = df['Context'].apply(text_normalization)

# all the stop words we have
stop = stopwords.words('english')


def stopword_(text):
    tag_list = pos_tag(nltk.word_tokenize(text), tagset=None)
    stop = stopwords.words('english')
    lema = wordnet.WordNetLemmatizer()
    lema_word = []
    for token, pos_token in tag_list:
        if token in stop:
            continue
        if pos_token.startswith('V'):
            pos_val = 'v'
        elif pos_token.startswith('J'):
            pos_val = 'a'
        elif pos_token.startswith('R'):
            pos_val = 'r'
        else:
            pos_val = 'n'
        lema_token = lema.lemmatize(token, pos_val)
        lema_word.append(lema_token)
    return " ".join(lema_word)


cv = CountVectorizer()
X = cv.fit_transform(df['lemmatized_text']).toarray()
features = cv.get_feature_names()
df_bow = pd.DataFrame(X, columns=features)


def chat_bow(text):
    s = stopword_(text)
    lemma = text_normalization(s)
    bow = cv.transform([lemma]).toarray()
    cosine_value = 1 - pairwise_distances(df_bow, bow, metric='cosine')
    index_value = cosine_value.argmax()
    return df['Text Response'].loc[index_value]