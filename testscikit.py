from sklearn import datasets
from sklearn import tree
from sklearn.tree import export_text
import numpy as np 
import pandas as pd
input_file = "economictestdata.csv"
df = pd.read_csv(input_file, header = 0)
numpy_array = df.to_numpy()
test_file = datasets.load_files(numpy_array)
iris = datasets.load_iris()
X, y = iris.data, iris.target
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X,y)
r = export_text(clf, feature_names=iris['feature_names'])
print(r)