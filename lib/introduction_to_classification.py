#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
# pip install -U scikit-learn
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


# In[ ]:


def load_dataset(file_name, label_column):
    df = pd.read_csv(file_name)
    X = df[df.columns[df.columns != label_column]]
    y = df[label_column]
    return X, y


# In[ ]:


def split_to_train_and_test(X, y, test_ratio, rand_state):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_ratio, random_state=rand_state)
    return X_train, X_test, y_train, y_test
    


# In[ ]:


def scale_features(X_train, scale_type):
    if scale_type == "minmax":
        scaler = MinMaxScaler(feature_range=(0, 1))
        X_train_scaled = scaler.fit_transform(X_train)
    if scale_type == "standard":
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
    return scaler, X_train_scaled


# In[ ]:


def scale_test_features(X_test, scaler):
    X_test_scaled = scaler.transform(X_test)
    return X_test_scaled
    


# In[ ]:


def train_classifier(X_train, y_train):
    return LogisticRegression().fit(X_train, y_train)


# In[ ]:


def predict(classifier, X_test, y_test):
    y_pred=classifier.predict(X_test)
    return pd.DataFrame({"Actual":y_test,"Predicted":y_pred})


# In[ ]:




