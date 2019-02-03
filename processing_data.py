# -*- coding: utf-8 -*-
"""NBC Draft Pred

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FduXTtlJ4u11cx1M0S3rXTHcor8yOfBd
"""
import pandas as pd
from sklearn_pandas import CategoricalImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Imputer
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split

X = pd.read_csv("./data_loader/data/training_data/player_stats_raw_features.csv")

from data_loader.Draft import Draft
from data_loader.Applicants import Applicants
draft = Draft()
applicants = Applicants()

player_box = pd.read_csv("./data_loader/data/ncaa/player_box.csv")
player_info = pd.read_csv("./data_loader/data/ncaa/player_info.csv")

# Filter out unwanted values
player_box = player_box[player_box['player_id']!=-101]
player_box = player_box[~player_box['player_id'].isnull()]
player_box = player_box[player_box['season']!=None]
player_box = player_box[player_box['season']!=2018]

player_info = player_info[player_info['player_id']!=-101]
player_info = player_info[~player_info['player_id'].isnull()]
player_info = player_info[player_info['season']!=None]
player_info = player_info[player_info['season']!=2018]
player_info = player_info[~player_info['first_name'].isnull()]
player_info = player_info[~player_info['last_name'].isnull()]

# Combine the two datasets
player_box["player_id_AND_season"] = player_box["player_id"].map(int).map(str) + "_AND_" + player_box["season"].map(int).map(str)
player_info["player_id_AND_season"] = player_info["player_id"].map(int).map(str) + "_AND_" + player_info["season"].map(int).map(str)
player_stats = pd.merge(player_box, player_info, on='player_id_AND_season', how='outer')
player_stats = player_stats.dropna()

# Get only drafted players
player_stats = applicants.join(player_stats)

# Add drafted categorical value
player_stats = draft.join(player_stats)

player_stats.to_csv('./data_loader/data/ncaa/player_stats.csv')

num_attribs = ['pts', 'fga', 'fga3', 'fgm', 'fgm3', 'fta', 'ftm', 'ast', 'blk', 'stl', 'dreb', 'oreb', 'reb', 'pf', 'tf', 'tov', 'mins_played', 'grade_level', 'division', 'height_in']
cat_attribs = ["school", "conference", "position"]

num_pipeline = Pipeline([
        ('imputer', Imputer(strategy="median")),
        ('std_scaler', StandardScaler())
    ])

cat_pipeline = Pipeline([
        ('imputer', CategoricalImputer()),
        ("cat", OneHotEncoder(handle_unknown='ignore'))
])

full_pipeline = ColumnTransformer([
        ("num", num_pipeline, num_attribs),
        # ('imputer', CategoricalImputer(), cat_attribs),
        ("cat", OneHotEncoder(), cat_attribs)
])

working = full_pipeline.fit_transform(X)
np.savetxt("player_stats_features.csv", working, delimiter=",")


X, y = pd.read_csv("./data_loader/data/training_data/player_stats_features.csv", index_col=0), pd.read_csv(
        "./data_loader/data/training_data/player_stats_labels.csv", index_col=0)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

for dataset, name in [(X_train, "X_train"), (X_test, "X_test"), (y_train, "y_train"), (y_test, "y_test")]:
        dataset.to_csv("data_loader/data/training_data/" + name + ".csv")