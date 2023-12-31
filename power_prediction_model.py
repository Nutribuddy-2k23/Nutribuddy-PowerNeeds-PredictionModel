# -*- coding: utf-8 -*-
"""power_prediction_model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fgOiRLc2R7UzoBxKTiS6dWY4eR23uN0o
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.impute import SimpleImputer

from google.colab import drive
drive.mount('/content/drive')

# Step 1: Data Preprocessing
# Load your dataset (replace 'your_dataset.csv' with the actual file path)
df = pd.read_csv('/content/power_needs.csv')

print(df.head())

# Getting last 3 rows from df
df_last_3 = df.tail(3)

# Printing df_last_3
print(df_last_3)

# Handle missing values (if any)
# For simplicity, we'll fill missing values with the mean for numerical columns
df.fillna(df.mean(), inplace=True)

print(df.head())

print(df.head())

# Drop columns that are not relevant for prediction (if any)
df = df.drop(['entry_id'], axis=1)

print(df.head())

# Define features and target variables for power needs prediction
X_power = df[['Water Needs(Litres)', 'Voltage (V)(volts)', 'Motor Efficiency(%)', 'Motor Capacity (P)(hp)', 'Maximum Flow Rate of the Motor(Liters per hour)']]
y_power = df['Power needs(KW)']

# Split the data into training and testing sets for both water and power needs
X_train_power, X_test_power, y_train_power, y_test_power = train_test_split(X_power, y_power, test_size=0.2, random_state=42)

# Step 4: Selecting a Model
model = LinearRegression()  # Linear Regression is chosen as an example. You can try different models.

# Step 5: Model Training
model.fit(X_train_power, y_train_power)

# Step 6: Model Evaluation
y_pred = model.predict(X_test_power)
mae = mean_absolute_error(y_test_power, y_pred)
mse = mean_squared_error(y_test_power, y_pred)
r2 = r2_score(y_test_power, y_pred)

print(f'Mean Absolute Error: {mae}')
print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

train_score = model.score(X_train_power, y_train_power)
val_score = model.score(X_test_power, y_test_power)

print(f"Training R-squared: {train_score}")
print(f"Validation R-squared: {val_score}")

from sklearn.model_selection import cross_val_score

# Perform k-fold cross-validation
scores = cross_val_score(model, X_power, y_power, cv=5)  # 5-fold cross-validation
print(f"Cross-validated R-squared scores: {scores}")

import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import learning_curve

# Generate learning curves
train_sizes, train_scores, val_scores = learning_curve(model, X_power, y_power, cv=5)

# Plot learning curves
plt.plot(train_sizes, np.mean(train_scores, axis=1), label='Training score')
plt.plot(train_sizes, np.mean(val_scores, axis=1), label='Validation score')
plt.xlabel('Training examples')
plt.ylabel('R-squared')
plt.legend(loc='best')
plt.show()

from sklearn.linear_model import Ridge

# Use Ridge regression with regularization
ridge_model = Ridge(alpha=1.0)  # Adjust alpha as needed
ridge_model.fit(X_train_power, y_train_power)
ridge_train_score = ridge_model.score(X_train_power, y_train_power)
ridge_val_score = ridge_model.score(X_test_power, y_test_power)

print(f"Ridge Training R-squared: {ridge_train_score}")
print(f"Ridge Validation R-squared: {ridge_val_score}")

# Assuming you have a separate test set X_test and y_test
test_score = model.score(X_test_power, y_test_power)
print(f"Test R-squared: {test_score}")

# Assuming 'X_train' is your DataFrame used for training
features_used = X_train_power.columns.tolist()

print("Features used during training:")
for feature in features_used:
    print(feature)

import pandas as pd

# Assuming X_new is a DataFrame
X_new = pd.DataFrame({
    'Water Needs(Litres)': [90, 105, 95],
    'Voltage (V)(volts)': [220, 220, 220],
    'Motor Efficiency(%)': [85, 85, 85],
    'Motor Capacity (P)(hp)': [0.5, 0.5, 0.5],
    'Maximum Flow Rate of the Motor(Liters per hour)': [1800, 1800, 1800]
    # Add other features as needed
})

# Now, you can use your trained model to make predictions
predictions = model.predict(X_new)

print(predictions)

y_train_pred = model.predict(X_train_power)
y_test_pred = model.predict(X_test_power)

# Step 3: Evaluate the model
train_mse = mean_squared_error(y_train_power, y_train_pred)
test_mse = mean_squared_error(y_test_power, y_test_pred)

print(f"Training Mean Squared Error: {train_mse}")
print(f"Testing Mean Squared Error: {test_mse}")

r_squared = r2_score(y_test_power, y_test_pred)

print(f"R-squared (coefficient of determination): {r_squared}")