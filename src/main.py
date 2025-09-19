location_data = {
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
