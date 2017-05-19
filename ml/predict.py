from concurrent.futures import ProcessPoolExecutor
import pandas as pd
import numpy as np
import csv
from sklearn import datasets, metrics, svm
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, f1_score
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier, RadiusNeighborsClassifier
import matplotlib.pyplot as plt
from sklearn.feature_selection import SelectKBest, chi2, f_classif
import sys

'''
USAGE: python predict.py samples.csv targets.csv [percentage you want to test on (< 1)]
'''

# Read in csv files
samples = pd.read_csv(sys.argv[1])
#samples = np.ravel(n_samples)
targets = pd.read_csv(sys.argv[2])

# Read in percentage to test on
ts = float(sys.argv[3])

# Breaks data ino training and testing data, then finds accuracy scores for each f value and places them within list
a_train, a_test, b_train, b_test = train_test_split(samples, targets, test_size=ts, random_state=0)

# Where values are predicted and accuracy scores are extracted

# Random Forest Algorithm
def rnd_forest():
    forr = RandomForestClassifier(n_estimators=35)
    forr.fit(a_train, b_train.values.ravel())
    rfc_pred = forr.predict(a_test)
    acc = metrics.accuracy_score(b_test, rfc_pred)

    print "Random Forest Accuracy score: {0}".format(acc)

# Ada Boost Algorithm
def ada_boost():
    ada = AdaBoostClassifier(n_estimators=80)
    ada.fit(a_train, b_train.values.ravel())
    rfc_pred = ada.predict(a_test)
    acc = metrics.accuracy_score(b_test, rfc_pred)

    print "Ada Boost Accuracy score: {0}".format(acc)

# Extra Trees algorithm
def extra_trees():
    trees = ExtraTreesClassifier(n_estimators=80)
    trees.fit(a_train, b_train.values.ravel())
    rfc_pred = trees.predict(a_test)
    acc = metrics.accuracy_score(b_test, rfc_pred)

    print "Extra Trees Accuracy score: {0}".format(acc)

# K-Nearest Neighbors Algorithm
def k_neighbors():
    trees = KNeighborsClassifier(n_neighbors=20)
    trees.fit(a_train, b_train.values.ravel())
    rfc_pred = trees.predict(a_test)
    acc = metrics.accuracy_score(b_test, rfc_pred)

    print "K-Nearest Neighbors Accuracy score: {0}".format(acc)

print ""

# Parallelize the predictions by creating a separate process for each algorithm
with ProcessPoolExecutor(max_workers=4) as e:
    e.submit(rnd_forest)
    e.submit(ada_boost)
    e.submit(extra_trees)
    e.submit(k_neighbors)

print ""
exit()
