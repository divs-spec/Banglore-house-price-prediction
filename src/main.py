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

import pandas as pd
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
    
