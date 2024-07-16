import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import requests
import io

# Function to call the UV Index API


def get_uv_index_data(city, state):
    url = f"https://data.epa.gov/efservice/getEnvirofactsUVHOURLY/CITY/{city.upper()}/STATE/{state.upper()}/CSV"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None


# uv index for phx
city = "phoenix"
state = "az"
uv_data = get_uv_index_data(city, state)

# convert to csv
if uv_data:
    uv_df = pd.read_csv(io.StringIO(uv_data))
    uv_df.to_csv('phoenix_uv_index.csv', index=False)
    print("UV Index data saved to 'phoenix_uv_index.csv'.")
else:
    print("Failed to retrieve UV Index data.")

# load datasets
uv_index_data = pd.read_csv('phoenix_uv_index.csv')
zoning_laws_data = pd.read_csv('Zoning_Index.csv')
tree_canopy_data = pd.read_csv('phx_treeLocations.csv')
walkable_areas_data = pd.read_csv('Walkable_Urban_Code.csv')

# print check
print("UV Index Data:\n", uv_index_data.head())
print("Zoning Laws Data:\n", zoning_laws_data.head())
print("Tree Canopy Data:\n", tree_canopy_data.head())
print("Walkable Areas Data:\n", walkable_areas_data.head())

# idk chat gpt asked me to do this
uv_index_data['DATE TIME'] = pd.to_datetime(uv_index_data['DATE TIME'])
uv_index_data['DATE'] = uv_index_data['DATE TIME'].dt.date
daily_uv_index = uv_index_data.groupby('DATE')['UV VALUE'].mean().reset_index()
daily_uv_index.rename(columns={'UV VALUE': 'UV_Index'}, inplace=True)
daily_uv_index['Region'] = 'Phoenix'

#  idk chat gpt asked me to do this
tree_canopy_summary = tree_canopy_data.groupby('city').agg({
    'height_M': 'mean',
    'diameter_breast_height_CM': 'mean'
}).reset_index()
tree_canopy_summary.rename(columns={'height_M': 'Avg_Tree_Height',
                           'diameter_breast_height_CM': 'Avg_Tree_Diameter'}, inplace=True)
tree_canopy_summary['Region'] = 'Phoenix'

# process walkable area
walkable_areas_summary = walkable_areas_data.copy()
walkable_areas_summary['Region'] = 'Phoenix'

walkable_areas_summary['Walkable_Areas'] = 1

# process zoning laws
zoning_laws_summary = zoning_laws_data[['OBJECTID', 'ZONING']].copy()
zoning_laws_summary['Region'] = 'Phoenix'

# summarize into one
zoning_laws_summary['Heat_Mitigation_Infra'] = 'High'

# merge data
merged_data = daily_uv_index.merge(zoning_laws_summary, on='Region') \
                            .merge(tree_canopy_summary, on='Region') \
                            .merge(walkable_areas_summary, on='Region')

# print all merged
print("Merged Data columns:", merged_data.columns)

# select features
features = ['UV_Index', 'ZONING', 'Avg_Tree_Height',
            'Avg_Tree_Diameter', 'Walkable_Areas']
X = merged_data[features]
#
y = merged_data['Heat_Mitigation_Infra']

# encode variables
X = pd.get_dummies(X, drop_first=True)

# train and split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# train
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

#
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')
print('Classification Report:')
print(classification_report(y_test, y_pred))

joblib.dump(model, 'decision_tree_model.pkl')

loaded_model = joblib.load('decision_tree_model.pkl')


def predict_infrastructure(data):
    new_data = pd.DataFrame(data)
    new_data = pd.get_dummies(new_data)
    new_data = new_data.reindex(columns=X_train.columns, fill_value=0)
    prediction = loaded_model.predict(new_data)
    return prediction


new_area_data = [
    {'UV_Index': 5, 'ZONING': 'Residential', 'Avg_Tree_Height': 5.0,
        'Avg_Tree_Diameter': 10.0, 'Walkable_Areas': 1},
    {'UV_Index': 8, 'ZONING': 'Commercial', 'Avg_Tree_Height': 6.0,
        'Avg_Tree_Diameter': 15.0, 'Walkable_Areas': 0}
]

predictions = predict_infrastructure(new_area_data)
for i, pred in enumerate(predictions):
    print(f'Predicted Heat Mitigating Infrastructure for area {i+1}: {pred}')
