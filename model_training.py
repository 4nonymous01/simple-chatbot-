import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow import keras
import joblib

# Load the dataset
df = pd.read_csv('car_prices.csv')

# Separate company from 'name' column
df['company'] = df['name'].apply(lambda x: x.split()[0])

# One-hot encoding for categorical variables, including company
df_encoded = pd.get_dummies(df, columns=['company', 'fuel', 'seller_type', 'transmission', 'owner'], drop_first=True)

# Feature selection
X = df_encoded[['year', 'km_driven', 'fuel_Diesel', 'fuel_LPG', 'fuel_Petrol', 
                'seller_type_Individual', 'seller_type_Trustmark Dealer', 
                'transmission_Manual', 'owner_Second Owner', 'owner_Third Owner', 
                'owner_Fourth & Above Owner', 'owner_Test Drive Car'] + 
               [col for col in df_encoded.columns if col.startswith('company_')]]
y = df_encoded['selling_price']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define the model
model = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(X_train_scaled.shape[1],)),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(1)  # Output layer for price prediction
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train_scaled, y_train, epochs=100, validation_split=0.2)

# Save the model using the new .keras format
model.save('car_price_model.keras')

# Save the scaler
joblib.dump(scaler, 'scaler.pkl')
