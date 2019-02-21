from sklearn.externals import joblib
from sklearn.tree import export_graphviz
from configs import feature_names

clf = joblib.load("./models/RandomForestClassifier.pkl")
estimator = clf.estimators_[0]

# Export as dot file
export_graphviz(estimator, out_file='tree.dot',
                feature_names = feature_names,
                class_names = ["In", "Out"],
                rounded = True, proportion = False,
                precision = 2, filled = True)

# Convert to png using system command (requires Graphviz)
from subprocess import call
call(['dot', '-Tpng', 'tree.dot', '-o', 'tree.png', '-Gdpi=600'])

# Display in jupyter notebook
from IPython.display import Image
Image(filename = 'tree.png')