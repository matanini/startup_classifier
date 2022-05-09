# --------------------------- RUN THIS CODE CELL -------------------------------------

# --------
# imports and setup 
# Use the following libraries for the assignment, when needed:
# --------
import re
import os

import pandas as pd
import numpy as np

import sklearn 
from sklearn import preprocessing, metrics, naive_bayes, pipeline, feature_extraction
from sklearn.feature_extraction import text
from sklearn.preprocessing import Normalizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB 
from sklearn.pipeline import Pipeline


from sklearn import neighbors, tree, ensemble, naive_bayes, svm
# *** KNN
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn import metrics
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def person_quotation_pattern_extraction(raw_text):
    extracted_person_name, extracted_quotation = None, None
    
    pattern_quote = r'"(.*)"'
    
    pattern_name = '([A-Z].\s?\w+\s\w+)'
    
    quotation = re.search(pattern_quote,raw_text)
    if quotation:
        extracted_quotation = quotation.group(1)
        text = raw_text.replace(f'"{extracted_quotation}"', "")
        
        name = re.search(pattern_name,text)
        if name:
            extracted_person_name = name.group(1)
            
    return extracted_person_name, extracted_quotation


def transfer_raw_text_to_dataframe(filename):
    columns = ['person_name', 'extracted_text']
    rows = []
    with open(filename, 'r') as file:
        for row in file.readlines():
            name, quote = person_quotation_pattern_extraction(row)
            rows.append([name, quote])
    return pd.DataFrame(np.array(rows),columns=columns)
        


def create_simple_pipeline():
    return Pipeline([('vect', CountVectorizer()),('clf', MultinomialNB())])

def fit(clf_pipeline, df_train):
    clf_pipeline.fit(df_train['extracted_text'], df_train['person_name'])


def predict(clf_trained_pipeline, x_test):
    return clf_trained_pipeline.predict(x_test)


def evaluate_accuracy(y_test, y_predicted):
    return accuracy_score(y_pred=y_predicted ,y_true=y_test)
