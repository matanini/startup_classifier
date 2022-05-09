#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt



# In[ ]:


def load_csv(file_name,column_names):
    with open(file_name) as file:
        df = pd.read_csv(file)
        return df[column_names]


# In[ ]:


def remove_duplicates(df, dup_col_name):
    return df.drop_duplicates(subset=dup_col_name).copy()


# In[ ]:


def remove_missing_str_val_rows(df, string_cols):
    for col in string_cols:
        df[col] = df[col].dropna()
    return df.copy()


# In[ ]:


def repair_numeric_missing_vals(df, numeric_cols):
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())
    return df.copy()


# In[1]:


def get_frequent_elements(df, col_name, num_top_elements):
    return df[col_name].value_counts()[:num_top_elements].sort_index()


# In[ ]:


def one_dim_plot(sr, plot_type, axis):
    sr.plot(kind=plot_type, ax = axis)


# In[ ]:


def plot_frequent_elements(df, df_in_params):
    fig, axes = plt.subplots(1,3, figsize=(20,5))
    for i, row in df_in_params.iterrows():
        sr = get_frequent_elements(df, row['col_name'], row['num_top_elements'])
        one_dim_plot(sr, row['plot_type'], axes[i])


# In[ ]:


def cross_tabulation(df, col_name, other_col_name):
    return pd.crosstab(df[col_name], df[other_col_name], normalize='index')


# In[ ]:


def plot_cross_tabulation(df, col_names, other_col_name):
    fig, axes = plt.subplots(1,len(col_names), figsize=(20,5))
    i=0
    for col_name in col_names:
        ct = cross_tabulation(df, col_name, other_col_name)
        ct.plot(kind='line', ax = axes[i])
        i=i+1


# In[ ]:


def get_highly_correlated_cols(df):
    correlations = []
    tuple_arr = []
    df_corr = df.corr()
    columns = df_corr.columns
#     print(df_corr)
    for column in columns:
        for index, row in df_corr.iterrows():
            a = columns.to_list().index(column)
            b = columns.to_list().index(row.name)
            if(row.name != column and row[column] >= 0.5 and a < b):
                correlations.append(row[column])
                tuple_arr.append((a, b))
#                 print(correlations, tuple_arr)
#                 print(row[column])
    return correlations, tuple_arr


# In[ ]:


def plot_high_correlated_scatters(df):
    correlations, tuple_arr = get_highly_correlated_cols(df)
    fig, axes = plt.subplots(1,len(tuple_arr), figsize=(20,5))
    i=0
    for cor, tup in zip(correlations, tuple_arr):
        col_name1 = df.columns.to_list()[tup[0]]
        col_name2 = df.columns.to_list()[tup[1]]
        df.plot(x = col_name1,
                y = col_name2,
                kind='scatter', 
                ax = axes[i], 
                title = f"corr('{col_name1}', '{col_name2}')={cor:4.2f}")
        i=i+1

