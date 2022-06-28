# ------------>>>>>>>> RUN THIS CODE CELL <<<<<<<<------------
# === CELL TYPE: IMPORTS AND SETUP 

import os                       # for testing use only

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
# --------cross-validation
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
# -------- classification
import sklearn
from sklearn import neighbors, tree, ensemble, naive_bayes, svm
# *** KNN
from sklearn.neighbors import KNeighborsClassifier
# *** Decision Tree; Random Forest
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
# *** Naive Bayes
from sklearn.naive_bayes import GaussianNB
# *** SVM classifier
from sklearn.svm import SVC
# --------  metrics:
from sklearn import metrics
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.metrics import make_scorer

def load_dataset(file_name):
    return pd.read_csv(file_name)


def transfer_str_to_numeric_vals(dataset):
    df = dataset.copy()
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    
    for col in df.columns:
        df[col] = sklearn.preprocessing.LabelEncoder().fit_transform(df[col])
    return df


def split_to_train_and_test(dataset, label_column, test_ratio, rand_state, stratify):
    X = dataset[dataset.columns[dataset.columns!=label_column]]
    y = dataset[label_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_ratio, random_state=rand_state, stratify=dataset[stratify])
    return X_train, X_test, y_train, y_test


def get_classifier_obj(classifier_name, params):
    if classifier_name == "KNN":
        if params:
            return KNeighborsClassifier(n_neighbors=params['n_neighbors'])
        else:
            return KNeighborsClassifier()
    if classifier_name == "naive_bayes":
        return GaussianNB()
    if classifier_name == "svm":
        return SVC()
    if classifier_name == "decision_tree":
        if params:
            return tree.DecisionTreeClassifier(max_depth=params['max_depth'], min_samples_split=params['min_samples_split'])
        else:
            return tree.DecisionTreeClassifier()
    if classifier_name == "random_forest":
        if params:
            return RandomForestClassifier(n_estimators=params['n_estimators'])
        else:
            return RandomForestClassifier()


def calc_evaluation_val(eval_metric, y_test, y_predicted):
    if eval_metric == "accuracy":
        evaluation_val = accuracy_score(y_test, y_predicted)
    if eval_metric == "precision":
        evaluation_val = precision_score(y_test, y_predicted)
    if eval_metric == "recall":
        evaluation_val = recall_score(y_test, y_predicted)
    if eval_metric == "f1":
        evaluation_val = f1_score(y_test, y_predicted)
    if eval_metric == "confusion_matrix":
        evaluation_val = confusion_matrix(y_test, y_predicted)
        
    
    return evaluation_val


def find_best_k_for_KNN(X_train, y_train):
    
    params = {'n_neighbors': [3, 7, 9, 11]}
    
    knn = get_classifier_obj("KNN", None)
    
    clf = GridSearchCV(knn, params, scoring=make_scorer(f1_score, greater_is_better=True))
    clf.fit(X_train, y_train)
    
    best_K, best_f1_val = clf.best_params_['n_neighbors'], clf.best_score_
    print(best_K, best_f1_val)
    return best_K, best_f1_val


def find_best_decision_tree_params(X_train, y_train):
    params = {'max_depth':[2,4,6], 'min_samples_split':[5,10,20] }
    df = tree.DecisionTreeClassifier()
    clf = GridSearchCV(df, params,scoring=make_scorer(metrics.f1_score, greater_is_better=True))
    clf.fit(X_train, y_train)
    return clf.best_params_['max_depth'], clf.best_params_['min_samples_split'] , clf.best_score_


def find_best_random_forest_num_estimators(X_train, y_train):
    parameters = {'n_estimators':[11,51,71] }
    rf = RandomForestClassifier()
    clf = GridSearchCV(rf, parameters,scoring=make_scorer(f1_score, greater_is_better=True))
    clf.fit(X_train, y_train)
    return clf.best_params_['n_estimators'], clf.best_score_


def find_best_model(X_train, y_train, max_depth_val, min_samples_split_val):
    dt = tree.DecisionTreeClassifier(max_depth=max_depth_val, min_samples_split=min_samples_split_val)
    nb = GaussianNB()
    svm = SVC()
    
    scores = []
    algs = [dt,nb,svm]
    
    for alg in algs : 
        avg_val_score = cross_val_score(alg, X_train, y_train,scoring="recall", cv=10).mean()
        scores.append(avg_val_score)
    
    best_val = max(scores)
    best_clf = algs[scores.index(best_val)]
    return best_clf, best_val



