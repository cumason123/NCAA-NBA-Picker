from sklearn.externals import joblib
from sklearn.tree import export_graphviz
from configs import feature_names
from subprocess import call

clf = joblib.load("./models/RandomForestClassifier.pkl")

for i in range(len(clf.estimators_)):
    # Export as dot file
    export_graphviz(clf.estimators_[i], out_file=f'./trees/tree{i}.dot',
                    feature_names = feature_names,
                    class_names = ["In", "Out"],
                    rounded = True, proportion = False,
                    precision = 2, filled = True)

    # Convert to png using system command (requires Graphviz)
    call(['dot', '-Tpng', f'./trees/tree{i}.dot', '-o', f'./trees/tree{i}.png', '-Gdpi=600'])

    # # Display in jupyter notebook
    # from IPython.display import Image
    # Image(filename = 'tree.png')