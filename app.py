# app.py
from flask import Flask, render_template, request
import joblib
import tensorflow as tf
from tensorflow import keras

app = Flask(__name__)

# Load the model and scaler
model = keras.models.load_model(r'C:\Users\Pruthu patel\Desktop\car_price_pridection\models\car_price_model.keras')
scaler = joblib.load(r'C:\Users\Pruthu patel\Desktop\car_price_pridection\models\scaler.pkl')

# Unique company names for selection
companies = ["Maruti", "Hyundai", "Datsun", "Honda", "Tata", "Chevrolet", "Toyota",
             "Jaguar", "Mercedes-Benz", "Audi", "Skoda", "Jeep", "BMW", "Mahindra",
             "Ford", "Nissan", "Renault", "Fiat", "Volkswagen", "Volvo", "Mitsubishi",
             "Land", "Daewoo", "MG", "Force", "Isuzu", "OpelCorsa", "Ambassador", "Kia"]

# Company price multiplier dictionary
company_price_multiplier = {
    "BMW": 1.5, "Mercedes-Benz": 1.4, "Audi": 1.3, "Toyota": 1.2, "Honda": 1.1,
    "Hyundai": 1.0, "Maruti": 0.9, "Tata": 0.8, "Ford": 0.8, "Skoda": 1.0,
    "Volkswagen": 1.0, "Nissan": 0.9, "Renault": 0.9, "Chevrolet": 0.85,
    "Datsun": 0.85, "Jeep": 1.2, "Jaguar": 1.4, "Mahindra": 0.9, "Fiat": 0.85,
    "Volvo": 1.3, "Mitsubishi": 1.0, "Land": 1.4, "Daewoo": 0.8, "MG": 0.95,
    "Force": 0.8, "Isuzu": 0.9, "OpelCorsa": 0.85, "Ambassador": 0.75, "Kia": 1.0
}

@app.route('/')
def home():
    return render_template('index.html', companies=companies)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Collect the selected company
        company = request.form.get('company')
        
        # Collect and organize features in the correct order
        year = request.form.get('year')
        km_driven = request.form.get('km_driven')

        if year is None or km_driven is None:
            return "Error: Please ensure all fields are filled."

        features = [
            float(year),
            float(km_driven),
        ]

        # Extract fuel type values (Petrol, Diesel, LPG)
        fuel = request.form.get('fuel')
        if fuel:
            fuel_values = list(map(float, fuel.split(',')))
            features.extend(fuel_values)
        else:
            return "Error: Fuel type is missing."

        # Extract seller type values (Dealer, Individual, Trustmark Dealer)
        seller_type = request.form.get('seller_type')
        if seller_type:
            seller_type_values = list(map(float, seller_type.split(',')))
            features.extend(seller_type_values)
        else:
            return "Error: Seller type is missing."

        # Transmission
        transmission = request.form.get('transmission')
        if transmission is not None:
            features.append(float(transmission))
        else:
            return "Error: Transmission type is missing."

        # Extract owner type values
        owner = request.form.get('owner')
        if owner:
            owner_values = list(map(float, owner.split(',')))
            features.extend(owner_values)
        else:
            return "Error: Owner type is missing."
        
        # Scale the input features
        features_scaled = scaler.transform([features])
        
        # Make prediction
        prediction = model.predict(features_scaled)

        # Apply company-specific price multiplier
        multiplier = company_price_multiplier.get(company, 1.0)
        final_price = prediction[0][0] * multiplier

        # Return the predicted car price
        return f'Predicted Car Price: Rs {final_price:.2f}'
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
