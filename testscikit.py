# Load libraries
import pandas as pd
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation


"""input_file = "economictestdata.csv"
df = pd.read_csv(input_file, header = 0)
numpy_array = df.to_numpy()
#test_file = datasets.load_files(numpy_array)
iris = datasets.load_iris()
X, y = iris.data, iris.target
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X,y)
r = export_text(clf, feature_names=iris['feature_names'])"""

#ecostation decision tree
col_names = ['_id','X','Y','OBJECTID','FULL_ADDRE','WEBSITE','NAME','DESCRIPTION']
data = pd.read_csv("ecostations.csv", header = None, names = col_names)
print(data.columns)
feature_cols = ['X', 'Y']
X = data[feature_cols]
y = data.DESCRIPTION
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size = 0.375, random_state = 1)
clf = DecisionTreeClassifier()
clf = clf.fit(x_train, y_train)
y_pred = clf.predict(x_test)
# Model Accuracy, how often is the classifier correct?
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
