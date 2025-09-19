'''location_data = {
    'Whitefield': {
        'base_price': 30,
        'price_per_bhk': 25
    },
    'Sarjapur Road': {
        'base_price': 45,
        'price_per_bhk': 30
    },
    'Electronic City': {
        'base_price': 25,
        'price_per_bhk': 20
    }
}

def calculate_price(location, bhk):

    # First, check if the provided 'location' is a key in our main dictionary.
    if location in location_data:
        # If the location exists, retrieve its specific data.
        data = location_data[location]
        base_price = data['base_price']
        price_per_bhk = data['price_per_bhk']
        
        # Apply the formula: Total Price = Base Price + (BHK * Price per BHK)
        total_price = base_price + (bhk * price_per_bhk)
        
        # Return the success message using an f-string for easy formatting.
        return f"The calculated price for a {bhk} BHK in {location} is {total_price} Lakhs."
    else:
        # This 'else' runs if the location was not found in the first 'if' check.
        return f"Sorry, we do not have pricing data for the location '{location}'."

if __name__ == "__main__":
    price1 = calculate_price('Whitefield', 2)
    print(price1)

    price2 = calculate_price('Marathahalli', 3)
    print(price2)

    price3 = calculate_price('Sarjapur Road', 3)
    print(price3)
'''

'''import pandas as pd
import numpy as np

def convert_sqft_to_num(x):
        
    # Split the string by the '-' character
    tokens = x.split('-')
    
    # If the split results in two parts, it's a range
    if len(tokens) == 2:
        # Calculate the average of the two numbers in the range
        return (float(tokens[0]) + float(tokens[1])) / 2
    
    # Handle regular numbers and other non-numeric cases
    try:
        # Try to convert the value directly to a float
        return float(x)
    except:
        # If conversion fails (e.g., for 'Sq. Meter'), return None
        return None

# --- Main execution block ---
if __name__ == "__main__":
    # 1. Load the dataset
    try:
        df = pd.read_csv('Bengaluru_House_Data.csv')
    except FileNotFoundError:
        print("Error: 'Bengaluru_House_Data.csv' not found. Please make sure it's in the same directory.")
        exit()
    
    # 2. Drop unnecessary columns
    df_cleaned = df.drop(['area_type', 'society', 'balcony', 'availability'], axis='columns')
    
    # 3. Drop initial rows with missing values
    df_cleaned = df_cleaned.dropna()

    # 4. Create the 'bhk' column from the 'size' column
    # We use a lambda function to process each value in the 'size' column
    df_cleaned['bhk'] = df_cleaned['size'].apply(lambda x: int(x.split(' ')[0]))
    
    # We can now drop the original 'size' column as it's no longer needed
    df_cleaned = df_cleaned.drop('size', axis='columns')

    # 5. Apply the conversion function to the 'total_sqft' column
    df_cleaned['total_sqft'] = df_cleaned['total_sqft'].apply(convert_sqft_to_num)
    
    # Display info before the final drop
    print("--- Data types before final cleaning ---")
    df_cleaned.info()

    # 6. Drop any remaining nulls that might have been created by our function
    df_cleaned = df_cleaned.dropna()
    
    print("\n--- Data types after final cleaning ---")
    df_cleaned.info()

    # 7. Save the cleaned DataFrame to a new CSV file
    df_cleaned.to_csv('cleaned_bengaluru_house_data.csv', index=False)
    
    print("\nCleaned data has been successfully saved to 'cleaned_bengaluru_house_data.csv'")
    print("\n--- First 5 rows of cleaned data ---")
    print(df_cleaned.head())
    '''
from flask import Flask, request, render_template
import pickle
import json
import numpy as np
import os

# Create a Flask web application
app = Flask(__name__)

# --- Global variables to hold the model and data columns ---
__model = None
__data_columns = None
__locations = None

# Define the project root path using this file's location
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def load_saved_artifacts():
    """Loads the saved model and column names from disk using absolute paths."""
    print("Loading saved artifacts... start")
    global __data_columns
    global __locations
    global __model

    # Load the column names from columns.json
    columns_path = os.path.join(PROJECT_ROOT, "columns.json")
    with open(columns_path, "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]  # Locations start after sqft, bath, bhk

    # Load the trained model from the pickle file
    model_path = os.path.join(PROJECT_ROOT, "bangalore_house_price_model.pickle")
    with open(model_path, "rb") as f:
        __model = pickle.load(f)
    print("Loading saved artifacts... done")

# Load artifacts at the module level so they're ready during testing/import
load_saved_artifacts()

def get_estimated_price(location, sqft, bhk, bath):
    """Takes user inputs and returns a price prediction."""
    try:
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        loc_index = -1

    # Create input vector
    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk

    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)

# --- Define the routes for the web application ---

@app.route('/')
def home():
    return render_template('index.html', locations=__locations)

@app.route('/predict', methods=['POST'])
def predict():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])

    estimated_price = get_estimated_price(location, total_sqft, bhk, bath)

    return render_template(
        'index.html',
        prediction_text=f'Estimated Price: {estimated_price} Lakhs',
        locations=__locations
    )

# --- Run the application ---
if __name__ == "__main__":
    print("Starting Python Flask Server for Bangalore House Price Prediction...")
    app.run(host='0.0.0.0', port=3000, debug=True)


# Load the trained model
with open("bangalore_house_price_model.pickle", "rb") as f:
    model = pickle.load(f)

