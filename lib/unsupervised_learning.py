# ------------>>>>>>>> RUN THIS CODE CELL <<<<<<<<------------
# === CELL TYPE: IMPORTS AND SETUP 

import os                       # for testing use only

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
# pip install seaborn
import sklearn
from sklearn import cluster

from sklearn import metrics, preprocessing, neighbors, cluster
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster

from sklearn.neighbors import kneighbors_graph
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import silhouette_samples, silhouette_score


plt.rcParams['figure.figsize'] = (10, 6)
plt.style.use('ggplot')
# Create color maps
from matplotlib.colors import ListedColormap
cmap = ListedColormap(["#e41a1c","#984ea3","#a65628","#377eb8","#ffff33","#4daf4a","#ff7f00"])

def load_dataset(file_name):
    return pd.read_csv(file_name)


def remove_missing_values(dataset):
    df = dataset.copy()
    df.dropna(inplace=True)
    return df


def remove_duplicate_rows(dataset):
    df = dataset.copy()
    df.drop_duplicates(inplace=True)
    return df


def transfer_str_to_numeric_vals(dataset,str_col,id_col_to_remove):
    df = dataset.copy()
    df[str_col] = sklearn.preprocessing.LabelEncoder().fit_transform(df[str_col])
    df.drop(columns=id_col_to_remove, inplace=True, axis=1)
    
    return df


def scale_dataset(dataset):
    df = dataset.copy()
    scaler = StandardScaler()
    dataset_scaled = scaler.fit_transform(df)
    return dataset_scaled


def perform_k_means(dataset, num_clusters, init_val, n_init_val, rand_state):
    df = dataset.copy()
    model = KMeans(n_clusters=num_clusters, n_init=n_init_val, init=init_val, random_state=rand_state)
    predicted_vals = model.fit_predict(dataset)
    return model, predicted_vals


def perform_hierarchical_clustering(dataset, num_clusters, linkage_val):
    model = AgglomerativeClustering(n_clusters=num_clusters, linkage=linkage_val)
    predicted_vals = model.fit_predict(dataset)
    return model, predicted_vals


def perform_density_based_clustering(dataset, epsilon_val, minimum_samples_val):
    model = DBSCAN(eps=epsilon_val, min_samples=minimum_samples_val)
    predicted_vals = model.fit_predict(dataset)
    
    return model, predicted_vals


def get_best_init_params_for_k_means(dataset, num_clusters, init_options, n_init_options, rand_state):
    scores = []
    results = {}
    best_score, best_init_val, best_n_init_val = -1, None, None
    for n in n_init_options:
        for option in init_options:
            km, predicted_vals = perform_k_means(dataset, num_clusters, option, n, rand_state)
            score = km.inertia_
            scores.append(score)
            results[score] = {"option": option, "n": n}
    
    scores.sort(reverse=True)
    
    for i in range(1, len(scores)):
        score = scores[i]
        if(scores[i-1] / scores[i] > 1.01):
            best_score = scores[i]
        
    return best_score, results[best_score]['option'], results[best_score]['n']


def compare_number_of_clusters(dataset, num_cluster_options, init_val, n_init_val, rand_state):
    scores = []
    for k in num_cluster_options:
        km, predicted_vals = perform_k_means(dataset, k, init_val, n_init_val, rand_state)
        scores.append(km.inertia_)
    return scores


def get_best_num_of_clusters_for_k_means(dataset, num_cluster_options, init_val, n_init_val, rand_state):
    scores = []
    clusters = {}
    best_score=0
    for k in num_cluster_options:
        km, predicted_vals = perform_k_means(dataset, k, init_val, n_init_val, rand_state)
        score = silhouette_score(dataset, predicted_vals)
        clusters[score] = k
        scores.append(score)
        if(score>best_score):
            best_score = score
            num_clusters =k
    
    return best_score, num_clusters


def get_best_linkage_method(dataset, num_clusters, linkage_options):
    scores = []
    clusters = {}
    best_score=0
    best_linkage = None
    best_n = 0
    for linkage_val in linkage_options:
        for n in num_clusters:
            model, y_pred = perform_hierarchical_clustering(dataset, n, linkage_val)
            score = silhouette_score(dataset, y_pred)
            clusters[score] = linkage_val
            scores.append(score)
            if(score>best_score):
                best_score = score
                best_linkage = linkage_val
                best_n = n
            
    return best_score, best_linkage, best_n


def get_best_params_for_dbscan(dataset, eps_options, min_samples_options):
    scores = []
    results = {}
    
    for minimum_samples_val in min_samples_options:
        for epsilon_val in eps_options:
            model, predicted_vals = perform_density_based_clustering(dataset, epsilon_val, minimum_samples_val)
            score = silhouette_score(dataset, predicted_vals)
            scores.append(score)
            results[score] = {"minimum_samples_val": minimum_samples_val, "epsilon_val": epsilon_val}
    best_score = max(scores)
   
    return best_score, results[best_score]['epsilon_val'], results[best_score]['minimum_samples_val']
    
    
