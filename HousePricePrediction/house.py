import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Load the dataset (Ames Housing)
data = pd.read_csv("AmesHousing.csv")

# Quick feature engineering:
# Total rooms = bedrooms + full baths + half baths
data['TotalRooms'] = data['Bedroom AbvGr'] + data['Full Bath'] + data['Half Bath']

# Features we'll use for prediction
feature_cols = [
    'TotalRooms',
    'Neighborhood',    # location info
    'Gr Liv Area',     # above ground living area
    'Lot Area',        # lot size
    'Garage Cars',     # garage capacity
    'Year Built'       # construction year
]
target_col = 'SalePrice'

X = data[feature_cols]
y = data[target_col]

# Separate numeric & categorical columns
num_features = X.select_dtypes(include=['int64', 'float64']).columns
cat_features = X.select_dtypes(include=['object']).columns

# Numeric data preprocessing: fill missing values + scale
num_pipe = Pipeline([
    ('fillna', SimpleImputer(strategy='median')),
    ('scale', StandardScaler())
])

# Categorical data preprocessing: fill missing values + one-hot encode
cat_pipe = Pipeline([
    ('fillna', SimpleImputer(strategy='most_frequent')),
    ('encode', OneHotEncoder(handle_unknown='ignore'))
])

# Combine preprocessing for numeric and categorical features
preprocess = ColumnTransformer([
    ('nums', num_pipe, num_features),
    ('cats', cat_pipe, cat_features)
])

# Build the pipeline with preprocessing + Linear Regression model
model = Pipeline([
    ('prep', preprocess),
    ('linreg', LinearRegression())
])

# Split into train & test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Predictions
preds = model.predict(X_test)

# Evaluate (RMSE) – using the older sklearn syntax (no squared=False)
rmse = np.sqrt(mean_squared_error(y_test, preds))
print("\nLinear Regression RMSE: {:.2f}\n".format(rmse))

# Prepare a small preview table with location, total rooms, and predicted price
results = X_test.copy()
results['PredictedPrice'] = preds

print("Sample Predictions (first 10):")
for i, row in results.head(10).iterrows():
    print(
        f"Location: {row['Neighborhood']:<15} | "
        f"Total Rooms: {row['TotalRooms']:<2} | "
        f"Predicted Price: ${row['PredictedPrice']:,.2f}"
    )
