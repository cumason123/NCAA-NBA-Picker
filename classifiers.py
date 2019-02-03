import logging
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.externals import joblib

def train(save=False):
    X_train, y_train = pd.read_csv("./data_loader/data/training_data/X_train.csv", index_col=0), pd.read_csv("./data_loader/data/training_data/y_train.csv", index_col=0)
    y_train = y_train.values.reshape(-1,) #flatten the y arg to avoid warning
    log_clf = LogisticRegression(random_state=42)
    rnd_clf = RandomForestClassifier(random_state=42)
    svm_clf = SVC(probability=True, random_state=42)

    voting_clf = VotingClassifier(
        estimators=[('lr', log_clf), ('rf', rnd_clf), ('svc', svm_clf)],
        voting='soft', n_jobs=-1)

    voting_clf.fit(X_train, y_train)

    for clf in (log_clf, rnd_clf, svm_clf, voting_clf):
        clf.fit(X_train, y_train)
        path = Path('./models/' + clf.__class__.__name__ + '.pkl')
        joblib.dump(clf, path)

def prediction():
    X_test, y_test = pd.read_csv("./data_loader/data/training_data/X_test.csv", index_col=0), pd.read_csv("./data_loader/data/training_data/y_test.csv", index_col=0)
    y_test = y_test.values.reshape(-1,) #flatten the y arg to avoid warning

    for clf_name in ("LogisticRegression", "RandomForestClassifier", "SVC", "VotingClassifier"):
        path = "./models/" + clf_name + '.pkl'
        clf = joblib.load(path)
        y_pred = clf.predict(X_test)
        logging.info(clf.__class__.__name__)
        logging.info("accuracy: " + str(accuracy_score(y_test, y_pred)))
        logging.info("f1-score: " + str(f1_score(y_test, y_pred)))

if __name__ == '__main__':
    logging.basicConfig(filename='./models/running.log')
    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())
    train(save=False)
    prediction()