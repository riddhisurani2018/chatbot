import pandas as pd
import nltk
import numpy as np
import re
from nltk.stem import wordnet
from sklearn.feature_extraction.text import CountVectorizer
from nltk import pos_tag
from sklearn.metrics import pairwise_distances
from nltk.corpus import stopwords
import sqlite3

# Read sqlite query results into a pandas DataFrame
con = sqlite3.connect("/home/riddhi/Desktop/chatbot/chatbot/db.sqlite3")
df = pd.read_sql_query("SELECT * from accounts_text_keyword_arabic", con)
df = df.rename(columns={'desc_arabic': 'Text Response', 'keyword_value_arabic': 'Context'})
df = df.reindex(columns=['Context', 'Text Response'])


def text_normalization(text):
    text = str(text).lower()  # text to lower case
    tokens = nltk.word_tokenize(text)  # word tokenizing
    lema = wordnet.WordNetLemmatizer()  # intializing lemmatization
    tags_list = pos_tag(tokens, tagset=None)  # parts of speech
    lema_words = []  # empty list
    for token, pos_token in tags_list:
        if pos_token.startswith('V'):
            pos_val = 'v'
        elif pos_token.startswith('J'):
            pos_val = 'a'
        elif pos_token.startswith('R'):
            pos_val = 'r'
        else:
            pos_val = 'n'  # Noun
        lema_token = lema.lemmatize(token, pos_val)
        lema_words.append(lema_token)
    return " ".join(lema_words)


text_normalization(df['Context'])
df['lemmatized_text'] = df['Context'].apply(text_normalization)


def stopword_(text):
    tag_list = pos_tag(nltk.word_tokenize(text), tagset=None)
    stop = stopwords.words('arabic')
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


cv = CountVectorizer()  # intializing the count vectorizer
X = cv.fit_transform(df['lemmatized_text']).toarray()

features = cv.get_feature_names()
df_bow = pd.DataFrame(X, columns=features)


def chat_bow_arabic(text):
    s = stopword_(text)
    lemma = text_normalization(s)  # calling the function to perform text normalization
    bow = cv.transform([lemma]).toarray()  # applying bow
    cosine_value = 1 - pairwise_distances(df_bow, bow, metric='cosine')
    index_value = cosine_value.argmax()  # getting index value
    return df['Text Response'].loc[index_value]
