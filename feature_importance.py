import numpy as np
import matplotlib.pyplot as plt
from sklearn.externals import joblib
import configs

from sklearn.datasets import make_classification
from sklearn.ensemble import ExtraTreesClassifier

forest = joblib.load("./models/RandomForestClassifier.pkl")

importances = forest.feature_importances_
std = np.std([tree.feature_importances_ for tree in forest.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking:")

num_feature = len(configs.feature_names)
ordered = []
for f in range(num_feature):
    print("%d. feature %s (%f)" % (f + 1, configs.feature_names[indices[f]], importances[indices[f]]))
    ordered.append(configs.feature_names[indices[f]])
# Plot the feature importances of the forest
plt.figure(figsize=(40, 5))
plt.title("Feature importances")
plt.bar(range(num_feature), importances[indices],
       color="r", yerr=std[indices], align="center")

plt.xticks(range(num_feature), ordered)
plt.xlim([-1, num_feature])
plt.show()