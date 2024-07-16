# Load libraries
import pandas as pd
import numpy as np
from sklearn.tree import export_text
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation
import requests

"""input_file = "economictestdata.csv"
df = pd.read_csv(input_file, header = 0)
numpy_array = df.to_numpy()
#test_file = datasets.load_files(numpy_array)
iris = datasets.load_iris()
X, y = iris.data, iris.target
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X,y)
r = export_text(clf, feature_names=iris['feature_names'])"""

"""ecostation decision tree
col_names = ['_id','X','Y','OBJECTID','FULL_ADDRE','WEBSITE','NAME','DESCRIPTION']
data = pd.read_csv("ecostations.csv", header = None, names = col_names)
print(data.columns)
feature_cols = ['X', 'Y']
X = data[feature_cols]
y = data.DESCRIPTION
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size = 0.10, random_state = 1)
clf = DecisionTreeClassifier()
clf = clf.fit(x_train, y_train)
y_pred = clf.predict(x_test)
# Model Accuracy, how often is the classifier correct?
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))"""
#Everything above this point was used for practicing/testing purposes.


#zip_code.txt = a list of all zip codes in Phoenix
phoenix_zipcodes = open("Zip_Code_Stuff/zip_codes.txt", "r")
dict = {'ZIP': [], 'UV_VALUE': []}
zdf = pd.DataFrame(dict)
for z in phoenix_zipcodes:
    z = z.rstrip()
    avg_uv = 0
    url = "https://data.epa.gov/efservice/getEnvirofactsUVHOURLY/ZIP/"+z+"/JSON"
    response = requests.get(url)
    if response.status_code == 200:
        result = pd.DataFrame(response.json())
        zip_data = result[['UV_VALUE']].query('UV_VALUE > 2')
        avg_uv = zip_data['UV_VALUE'].mean()
        new_row = {'ZIP': z, 'UV_VALUE':avg_uv}
        zdf = zdf._append(new_row, ignore_index=True)


#decision tree
## I am setting the threshold for add infrastructure to be UV >= 7, but this can change
"""def add_infrastructure(row):
    return 1 if row['UV_VALUE'] >= 7 else 0    

zdf['target'] = zdf.apply(add_infrastructure, axis = 1)
uv_feature_cols = ['ZIP', 'UV_VALUE']
uvX = zdf[uv_feature_cols]
uvy = zdf['target']
uvx_train, uvx_test, uvy_train, uvy_test = train_test_split(uvX, uvy, test_size = 0.4, random_state = 1)
uv_clf = DecisionTreeClassifier()
uv_clf = uv_clf.fit(uvx_train, uvy_train)
uvy_pred = uv_clf.predict(uvx_test)
# Model Accuracy, how often is the classifier correct?
print("Accuracy:",metrics.accuracy_score(uvy_test, uvy_pred))
print(export_text(uv_clf))"""