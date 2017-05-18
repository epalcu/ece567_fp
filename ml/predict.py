from __future__ import division
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

# USAGE: python predict.py samples.csv targets.csv [percentage you want to test on (< 1)]

# Read in csv files
samples = pd.read_csv(sys.argv[1])
#samples = np.ravel(n_samples)
targets = pd.read_csv(sys.argv[2])

# Read in percentage to test on
ts = float(sys.argv[3])

# Breaks data ino training and testing data, then finds accuracy scores for each f value and places them within list
a_train, a_test, b_train, b_test = train_test_split(samples, targets, test_size=ts, random_state=0)

# Where values are predicted and accuracy and precsion scores are extracted
forr = RandomForestClassifier(n_estimators=35)
forr.fit(a_train, b_train.values.ravel())
rfc_pred = forr.predict(a_test)
acc = metrics.accuracy_score(b_test, rfc_pred)

print "Random Forest Accuracy score: {0}".format(acc)

forr = AdaBoostClassifier(n_estimators=80)
forr.fit(a_train, b_train.values.ravel())
rfc_pred = forr.predict(a_test)
acc = metrics.accuracy_score(b_test, rfc_pred)

print "Ada Boost Accuracy score: {0}".format(acc)
