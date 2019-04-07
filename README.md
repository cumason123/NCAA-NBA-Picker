# NCAA Dataset Analysis

## Background

This is a project born in the Google Cloud & NCAA hackathon on the week of Jan 26, 2019 at MIT. It won first place.

## Methodology

Our project includes the following components:
1. An ensemble classifier that predicts if NBA applicants would be successfully drafted by NBA teams based on their historical performance and personal background (school, team, etc.) See [classifiers.py](https://github.com/cumason123/NCAA-NBA-Picker/blob/master/classifiers.py) for classifiers. See the images in the "trees" folder for the visualization of the importance of features (based on one tree from the random forest). (The keys for the visualization is [here](https://docs.google.com/document/d/1OHZ4-4dDhNFdBlk1spDKVRteCM6fBitw20iP9TLOpYU/edit?usp=sharing))
2. An LSTM model to predict outcomes of future games. See  [Game_Prediction.ipynb](https://github.com/cumason123/NCAA-NBA-Picker/blob/master/Game_Prediction.ipynb "Game Prediction").

Note:
1. Since we only have a limited small-sized dataset, the results here are not fully realistic.

## Files

Scripts (according to the processing sequence)

- data_loader/DatasetsGenerator: a collections of scripts to preprocess the data, written by Curtis 
- processing_data.py: prepares the data for the machine learning models
- configs.py: the features
- **classifiers.py**: the machine learning classifiers
- **classifiers_visualization.py**: visualizes the trained model of the random forest

Other:

- models: the trained models
- **Game_Prediction.ipynb**: uses neural networks to predict outcomes of games
- transient: code that is no longer used, but kept for historic purposes

## Team

Our original team members are Curtis Mason, Jennifer (Jaehei) Kim, Julius Frost, Deren Singh, Zack Light (Yi Zhang). 

[Curtis Mason](https://github.com/cumason123 "Curtis Mason Github Profile"), [Julius Frost](https://github.com/juliusfrost "Julius Frost Github Profile"), [Zack Light (Yi Zhang)](https://zacklight.com "Zack Light (Yi Zhang)"), have contributed to this github repository.

License
----

MIT


