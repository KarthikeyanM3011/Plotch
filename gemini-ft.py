
from flask import Flask, request, jsonify
from google.oauth2 import service_account
import vertexai
import os
from vertexai.preview.generative_models import GenerativeModel
import json

app = Flask(__name__)

PROJECT_ID = '380777522230'
LOCATION = 'asia-south1'
ENDPOINT_ID = '5207080360961114112'

def init_vertexai():
    credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    if credentials_json:
        credentials_dict = credentials_json
        credentials = service_account.Credentials.from_service_account_info(credentials_dict)
    
    vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=credentials)
    
    system_instruction = '''
    ***System Instruction***:
    You are an Indian ecommerce assistant tasked with extracting key-value pairs from user queries and formatting them in JSON. Construct a JSON block with action_intent, filters, and prompt. Set action_intent to "search". The filters section should encompass various attributes: category_name defines the type of product, such as "sarees," "laptops," or "smartphones"; brand_name refers to the brand of the product if mentioned; price_min is the minimum price limit if specified using under, below, lower than, not higher than like words, while price_max is the maximum price limit indicated by above, exceeds; For the sort_by field, use top_selling for top-selling searches, new_arrivals for new or latest items, most_discounted for items with the highest discounts, distance for the closest or nearby options, lowest_price for the cheapest or "sasti" items, and highest_price for premium or luxury-related keywords. If no price_max is given then assign it with a amount that the product would cost in India. For price_max assign an estimated market cost of the product in India; provider_name includes the name of the seller or store if identifiable; colour denotes the color of the item, like "green" or "red"; material describes the material of the product, such as "cotton" or "leather" or any given in the query; pattern refers to any design patterns like "striped" or "floral"; size indicates the size of the product in terms of common sizing labels like "S," "M," or "L," while numeric_clothing_size refers to specific numerical sizes such as "38"; and gender specifies the intended gender for the product or given in the user query, such as "men" or "women" or "kids" or "unisex"; connectivity_technology means like "bluetooth" or "wi-fi" like connectivity technology. Ensure that the result is in pure English and that the language of the input is noted with the query.
    Filters should include: `category_name`, `brand_name`, `price_min`, `price_max`, `provider_name`, `query_entity_type`, `colour`, `material`, `pattern`, `size`, `gender`, `sort_by`, `numeric_clothing_size`, `shoe_size`, `neck_style`, `occasion`, `fit_type`, `sleeve_length`, `care_instructions`, `sleeve_type`, `weight`, `memory_RAM`, `storage`, `battery_capacity`, `seasons`, `model_year`, `cell_phone_features`, `veg_type`, `operating_system`, `pocket_type`, `special_features`, `air_conditioner_type`, `specialty_food_type`, `diet_type`, `condition`, `craft_type`, `connectivity_technology`, `ingredient`, `skin_tone`, `skin_type`, `finish`, `health_concern`, `health_benefit`, `topping`, `crust_type`, `formulation`, `hemline`, `shape`, `cuisine_type`.
    '''
    
    model_endpoint = f'projects/{PROJECT_ID}/locations/{LOCATION}/endpoints/{ENDPOINT_ID}'
    model = GenerativeModel(model_endpoint, system_instruction=[system_instruction])

    return model

model = init_vertexai()

@app.route('/intent', methods=['POST'])
def process_query():
    try:
        data = request.json
        query = data.get('query', '')

        if not query:
            return jsonify({'error': 'No query provided'}), 400

        response = model.generate_content(query)

        result = response.text

        return jsonify({'result': result})

    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
