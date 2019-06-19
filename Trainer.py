import sklearn
import pandas as pd
from sklearn import svm
import pickle
import numpy as np
from sklearn.metrics import classification_report
from sklearn.metrics import zero_one_loss
extracted_col = [u'diagnosis',
                   u'radius_mean',            u'texture_mean',
                u'perimeter_mean',               u'area_mean',
               u'smoothness_mean',        u'compactness_mean',
                u'concavity_mean',     u'concave points_mean',
                 u'symmetry_mean',  u'fractal_dimension_mean',
                    ]

csv_file = pd.read_csv("data.csv",encoding ="utf-8",skipinitialspace=True,usecols=extracted_col)
csv_file[u'diagnosis']=csv_file[u'diagnosis'].replace("M" , 1 , regex=True)
csv_file[u'diagnosis']=csv_file[u'diagnosis'].replace("B" , 0 , regex=True)
train, validate, test = np.split(csv_file.sample(frac=1), [int(.6*len(csv_file)), int(.8*len(csv_file))])
array = train.values
X = array[:,1:len(extracted_col)]
Y = array[:,0]
array_validate = validate.values
X_validate = array_validate[:,1:len(extracted_col)]
Y_validate= array_validate[:,0]
clf = svm.SVC()
clf.fit(X, Y)
pickle.dump(clf , open("breastcancer.model" ,"w"))
y_pred = clf.predict(X_validate)
print "Accuracy:", zero_one_loss(Y_validate, y_pred)
print "Classification report:"
print classification_report(Y_validate, y_pred)
