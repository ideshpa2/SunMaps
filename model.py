import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
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

# Function to process UV Index data


def process_uv_index_data(city, state):
    uv_data = get_uv_index_data(city, state)
    if uv_data:
        uv_df = pd.read_csv(io.StringIO(uv_data))
        uv_df.to_csv('phoenix_uv_index.csv', index=False)
        uv_df['DATE TIME'] = pd.to_datetime(uv_df['DATE TIME'])
        uv_df['DATE'] = uv_df['DATE TIME'].dt.date
        daily_uv_index = uv_df.groupby('DATE')['UV VALUE'].mean().reset_index()
        daily_uv_index.rename(columns={'UV VALUE': 'UV_Index'}, inplace=True)
        daily_uv_index['Region'] = 'Phoenix'
        return daily_uv_index
    else:
        print("Failed to retrieve UV Index data.")
        return None

# Function to process Tree Canopy data


def process_tree_canopy_data(file_path):
    tree_canopy_data = pd.read_csv(file_path)
    tree_canopy_summary = tree_canopy_data.groupby('city').agg({
        'height_M': 'mean',
        'diameter_breast_height_CM': 'mean'
    }).reset_index()
    tree_canopy_summary.rename(columns={'height_M': 'Avg_Tree_Height',
                                        'diameter_breast_height_CM': 'Avg_Tree_Diameter'}, inplace=True)
    tree_canopy_summary['Region'] = 'Phoenix'
    return tree_canopy_summary

# Function to process Walkable Areas data


def process_walkable_areas_data(file_path):
    walkable_areas_data = pd.read_csv(file_path)
    walkable_areas_data['Region'] = 'Phoenix'
    walkable_areas_data['Walkable_Areas'] = 1
    return walkable_areas_data

# Function to process Zoning Laws data


def process_zoning_laws_data(file_path):
    zoning_laws_data = pd.read_csv(file_path)
    zoning_laws_summary = zoning_laws_data[['OBJECTID', 'ZONING']].copy()
    zoning_laws_summary['Region'] = 'Phoenix'
    return zoning_laws_summary

# Function to process Average Precipitation data


def process_avg_precipitation_data(file_path):
    avg_precipitation_data = pd.read_csv(file_path)
    avg_precipitation_summary = avg_precipitation_data.groupby('LEGEND').agg({
        'ANNUAL_': 'mean'
    }).reset_index()
    avg_precipitation_summary.rename(
        columns={'ANNUAL_': 'Avg_Precipitation'}, inplace=True)
    avg_precipitation_summary['Region'] = 'Phoenix'
    return avg_precipitation_summary

# Function to determine heat mitigation infrastructure value


def determine_heat_mitigation_infra(row):
    if row['UV_Index'] > 7:
        return 'High'
    elif row['Avg_Tree_Height'] > 5 and row['Avg_Tree_Diameter'] > 10:
        return 'Medium'
    elif row['Walkable_Areas'] == 1:
        return 'Medium'
    else:
        return 'Low'


# Fetch and process data
daily_uv_index = process_uv_index_data('phoenix', 'az')
tree_canopy_summary = process_tree_canopy_data('phx_treeLocations.csv')
walkable_areas_summary = process_walkable_areas_data('Walkable_Urban_Code.csv')
zoning_laws_summary = process_zoning_laws_data('Zoning_Index.csv')
avg_precipitation_summary = process_avg_precipitation_data('precipitation.csv')

# Merge data
if daily_uv_index is not None:
    merged_data = daily_uv_index.merge(zoning_laws_summary, on='Region') \
                                .merge(tree_canopy_summary, on='Region') \
                                .merge(walkable_areas_summary, on='Region') \
                                .merge(avg_precipitation_summary, on='Region')

    # Fill missing values in merged data
    merged_data.fillna(0, inplace=True)

    # Apply the function to determine heat mitigation infrastructure value
    merged_data['Heat_Mitigation_Infra'] = merged_data.apply(
        determine_heat_mitigation_infra, axis=1)

    # Select features and target
    features = ['UV_Index', 'ZONING', 'Avg_Tree_Height',
                'Avg_Tree_Diameter', 'Walkable_Areas', 'Avg_Precipitation']
    X = merged_data[features]
    y = merged_data['Heat_Mitigation_Infra']

    # Encode variables
    X = pd.get_dummies(X, drop_first=True)

    # Train and split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    # Train model with cross-validation
    model = DecisionTreeClassifier()
    cross_val_scores = cross_val_score(model, X_train, y_train, cv=5)
    print(f'Cross-Validation Scores: {cross_val_scores}')
    print(f'Average Cross-Validation Score: {cross_val_scores.mean()}')

    # Fit the model and evaluate
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy}')
    print('Classification Report:')
    print(classification_report(y_test, y_pred))

    # Save model
    joblib.dump(model, 'decision_tree_model.pkl')

    # Function to predict new data and print recommendations
    def predict_infrastructure(data, model, columns):
        new_data = pd.DataFrame(data)
        new_data = pd.get_dummies(new_data)
        new_data = new_data.reindex(columns=columns, fill_value=0)

        # Perform predictions
        prediction = model.predict(new_data)

        # Override predictions based on conditions
        recommendations = []
        for i in range(len(new_data)):
            if 'ZONING_Residential' in new_data.columns and new_data.loc[i, 'ZONING_Residential'] == 1:
                recommendations.append(
                    'Residential: Solar panel installation, more trees, and green areas')
            elif 'ZONING_Commercial' in new_data.columns and new_data.loc[i, 'ZONING_Commercial'] == 1:
                recommendations.append(
                    'Commercial: Cool roofs, green walls, and urban trees')
            elif 'ZONING_Industrial' in new_data.columns and new_data.loc[i, 'ZONING_Industrial'] == 1:
                recommendations.append(
                    'Industrial: Reflective materials, water bodies, and green buffers')
            else:
                recommendations.append(prediction[i])

        return recommendations

    # Load model and make predictions
    loaded_model = joblib.load('decision_tree_model.pkl')

    # Example data based on typical values from the dataset
    new_area_data = [
        {'UV_Index': merged_data['UV_Index'].mean(), 'ZONING': 'Residential', 'Avg_Tree_Height': merged_data['Avg_Tree_Height'].mean(
        ), 'Avg_Tree_Diameter': merged_data['Avg_Tree_Diameter'].mean(), 'Walkable_Areas': 1, 'Avg_Precipitation': merged_data['Avg_Precipitation'].mean()},
        {'UV_Index': merged_data['UV_Index'].quantile(0.75), 'ZONING': 'Commercial', 'Avg_Tree_Height': merged_data['Avg_Tree_Height'].quantile(
            0.75), 'Avg_Tree_Diameter': merged_data['Avg_Tree_Diameter'].quantile(0.75), 'Walkable_Areas': 0, 'Avg_Precipitation': merged_data['Avg_Precipitation'].quantile(0.75)},
        {'UV_Index': merged_data['UV_Index'].quantile(0.25), 'ZONING': 'Industrial', 'Avg_Tree_Height': 0.0, 'Avg_Tree_Diameter': 0.0,
         'Walkable_Areas': 1, 'Avg_Precipitation': merged_data['Avg_Precipitation'].quantile(0.25)}
    ]

    predictions = predict_infrastructure(
        new_area_data, loaded_model, X_train.columns)

    # Print predictions with zoning type and detailed recommendations
    zoning_types = ['Residential', 'Commercial', 'Industrial']
    for i, pred in enumerate(predictions):
        if zoning_types[i] == 'Residential':
            print(
                f'Predicted Heat Mitigating Infrastructure for {zoning_types[i]} area: {pred} - Recommendations: Solar panel installation, more trees, and green areas')
        elif zoning_types[i] == 'Commercial':
            print(
                f'Predicted Heat Mitigating Infrastructure for {zoning_types[i]} area: {pred} - Recommendations: Cool roofs, green walls, and urban trees')
        elif zoning_types[i] == 'Industrial':
            print(
                f'Predicted Heat Mitigating Infrastructure for {zoning_types[i]} area: {pred} - Recommendations: Reflective materials, water bodies, and green buffers')
else:
    print("UV Index data is not available. Model training and prediction cannot proceed.")
