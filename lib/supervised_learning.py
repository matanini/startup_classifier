import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import r2_score, f1_score
from sklearn import preprocessing

def load_dataset(file_name, target_column):
    df = pd.read_csv(file_name)
    X = df[df.columns[df.columns != target_column]]
    y = df[target_column]
    return X, y


def train_1st_model(X_train, y_train):
    trained_model = LinearRegression().fit(X_train, y_train)
    return trained_model


def predict_1st(trained_1st_model, X_test):
    predicted_vals = trained_1st_model.predict(X_test)
    return predicted_vals


def evaluate_performance_1st(y_test,y_predicted):
    evaluate_value= r2_score(y_test, y_predicted)
    return evaluate_value


def train_2nd_model(X_train, y_train):
    trained_model = LogisticRegression().fit(X_train, y_train)
    return trained_model


def predict_2nd(trained_2nd_model, X_test):
    predicted_vals = trained_2nd_model.predict(X_test)
    return predicted_vals


def evaluate_performance_2nd(y_test,y_predicted):
    evaluate_value = f1_score(y_test, y_predicted)
    return evaluate_value


def manipulate_1st_feature_vector(X):
    X_copy = X.drop(['language','country'], axis=1).copy()
    X_copy['language'] = preprocessing.LabelEncoder().fit_transform(X['language'])
    X_copy['country'] = preprocessing.LabelEncoder().fit_transform(X['country'])
    X_copy = pd.get_dummies(X_copy, columns=['color'], prefix=['color'])
    
    X_copy = X_copy.drop(['language','country', 'title_year'], axis=1)
    
    bins = ['PG-13', 'R', 'PG', 'NC-17','G']
    labels =[1,2,3,4,5]
    X_copy['content_rating'].replace(bins, labels,inplace=True)
    
    likes = X_copy['director_facebook_likes']
    + X_copy['actor_3_facebook_likes']
    + X_copy['actor_1_facebook_likes']
    + X_copy['cast_total_facebook_likes']
    + X_copy['actor_2_facebook_likes']
    + X_copy['movie_facebook_likes']
    
    X_copy['director_facebook_likes'] = X_copy['director_facebook_likes']/likes
    X_copy['actor_3_facebook_likes'] = X_copy['actor_3_facebook_likes']/likes
    X_copy['actor_1_facebook_likes'] = X_copy['actor_1_facebook_likes']/likes
    X_copy['cast_total_facebook_likes'] = X_copy['cast_total_facebook_likes']/likes
    X_copy['actor_2_facebook_likes'] = X_copy['actor_2_facebook_likes']/likes
    X_copy['movie_facebook_likes'] = X_copy['movie_facebook_likes']/likes
    
    X_copy['likes_budget'] = likes/X_copy['budget']
    X_copy['likes_gross'] = likes/X_copy['gross']
    X_copy['users'] = X_copy['num_voted_users']/X_copy['num_user_for_reviews']
    X_copy['profit'] = X_copy['gross'] - X_copy['budget']
    
    processed_X = X_copy
    
    return processed_X
    
    
