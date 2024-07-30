# from flask import Flask, request, jsonify
# from google.oauth2 import service_account
# from google.auth.transport.requests import Request
# import requests
# import json

# app = Flask(__name__)

# SERVICE_ACCOUNT_FILE = './cartesian-service.json'

# def get_access_token():
#     """Obtain an access token using the service account credentials."""
#     try:
#         credentials = service_account.Credentials.from_service_account_file(
#             SERVICE_ACCOUNT_FILE,
#             scopes=['https://www.googleapis.com/auth/cloud-platform'],
#         )
#         credentials.refresh(Request())
#         return credentials.token
#     except Exception as e:
#         app.logger.error(f"Error obtaining access token: {e}")
#         return None

# @app.route('/intent', methods=['POST'])
# def process_query():
#     try:
#         data = request.json
#         query = data.get('query', '')

#         if not query:
#             return jsonify({'error': 'No query provided'}), 400

#         system_prompt = '''
#         ***System Instruction*** :
#         You are an Indian ecommerce assistant tasked with extracting key-value pairs from user queries and formatting them in JSON. Construct a JSON block with action_intent, filters, and prompt. Set action_intent to "search". The filters section should encompass various attributes: category_name defines the type of product, such as "sarees," "laptops," or "smartphones"; brand_name refers to the brand of the product if mentioned; price_min is the minimum price limit if specified using under, below, lower than, not higher than like words, while price_max is the maximum price limit indicated by above, exceeds;For the sort_by field, use top_selling for top-selling searches, new_arrivals for new or latest items, most_discounted for items with the highest discounts, distance for the closest or nearby options, lowest_price for the cheapest or "sasti" items, and highest_price for premium or luxury-related keywords.If no price_max is given then assign it with a amount that the product would cost in India.For price_max assign an estimated market cost of the product in India; provider_name includes the name of the seller or store if identifiable; colour denotes the color of the item, like "green" or "red"; material describes the material of the product, such as "cotton" or "leather" or any given in the query ; pattern refers to any design patterns like "striped" or "floral"; size indicates the size of the product in terms of common sizing labels like "S," "M," or "L," while numeric_clothing_size refers to specific numerical sizes such as "38"; and gender specifies the intended gender for the product or given in the user query, such as "men" or "women" or "kids" or "unisex";connectivity_technology means like "bluetooth" or "wi-fi" like connectivity technology. Ensure that the result is in pure English and that the language of the input is noted with the query.
#         Filters should include: `category_name`, `brand_name`, `price_min`, `price_max`, `provider_name`, `query_entity_type`, `colour`, `material`, `pattern`, `size`, `gender`, `sort_by`, `numeric_clothing_size`, `shoe_size`, `neck_style`, `occasion`, `fit_type`, `sleeve_length`, `care_instructions`, `sleeve_type`, `weight`, `memory_RAM`, `storage`, `battery_capacity`, `seasons`, `model_year`, `cell_phone_features`, `veg_type`, `operating_system`, `pocket_type`, `special_features`, `air_conditioner_type`, `specialty_food_type`, `diet_type`, `condition`, `craft_type`, `connectivity_technology`, `ingredient`, `skin_tone`, `skin_type`, `finish`, `health_concern`, `health_benefit`, `topping`, `crust_type`, `formulation`, `hemline`, `shape`, `cuisine_type`.

#         Example 1 : 
#             Input Query : Enakku pachai pudavai kaattu
#             Output : {"action_intent":"search","filters":{"category_name":"sarees","brand_name":"","price_min":"","price_max":"","provider_name":"","query_entity_type":"product","colour":"green","material":"","pattern":"","size":"","gender":"","sort_by":"top-selling","numeric_clothing_size":"","shoe_size":"","neck_style":"","occasion":"","fit_type":"","sleeve_length":"","care_instructions":"","sleeve_type":"","weight":"","memory_RAM":"","storage":"","battery_capacity":"","seasons":"","model_year":"","cell_phone_features":"","veg_type":"","operating_system":"","pocket_type":"","special_features":"","air_conditioner_type":"","specialty_food_type":"","diet_type":"","condition":"","craft_type":"","connectivity_technology":"","ingredient":"","skin_tone":"","skin_type":"","finish":"","health_concern":"","health_benefit":"","topping":"","crust_type":"","formulation":"","hemline":"","shape":"","cuisine_type":""},"prompt":"Enakku pachai pudavai kaattu"}

#         Example 2 :
#             Input Query : Show me cheap formal green sarees with polka dot work under 1500.
#             Output : {"action_intent":"search","filters":{"category_name":"sarees","brand_name":"","price_min":"","price_max":"1500","provider_name":"","query_entity_type":"product","colour":"green","material":"","pattern":"Polka dots","size":"","gender":"women","sort_by":"lowest_price","numeric_clothing_size":"","shoe_size":"","neck_style":"","occasion":"Formal","fit_type":"","sleeve_length":"","care_instructions":"","sleeve_type":"","weight":"","memory_RAM":"","storage":"","battery_capacity":"","seasons":"","model_year":"","cell_phone_features":"","veg_type":"","operating_system":"","pocket_type":"","special_features":"","air_conditioner_type":"","specialty_food_type":"","diet_type":"","condition":"","craft_type":"","connectivity_technology":"","ingredient":"","skin_tone":"","skin_type":"","finish":"","health_concern":"","health_benefit":"","topping":"","crust_type":"","formulation":"","hemline":"","shape":"","cuisine_type":""},"prompt":"Show me cheap formal green sarees with polka dot work"}
        
#         '''

#         json_payload = {
#             "contents": [
#                 {
#                     "role": "user",
#                     "parts": [
#                         {
#                             "text": f'''{system_prompt}    ***Input Query*** : {query}'''
#                         }
#                     ]
#                 }
#             ],
#             "generationConfig": {
#                 "maxOutputTokens": 2048,
#                 "temperature": 0.5,
#                 "top_p": 1,
#                 "top_k": 1
#             }
#         }

#         token = get_access_token()

#         if not token:
#             return jsonify({'error': 'Failed to obtain access token'}), 500

#         headers = {
#             'Authorization': f'Bearer {token}',
#             'Content-Type': 'application/json; charset=utf-8'
#         }

#         response = requests.post(
#             'https://asia-south1-aiplatform.googleapis.com/v1/projects/380777522230/locations/asia-south1/endpoints/5207080360961114112:generateContent',
#             headers=headers,
#             json=json_payload
#         )

#         if response.status_code == 403:
#             return jsonify({'error': 'Auth token is missing !'}), 403
#         elif response.status_code == 429:
#             return jsonify({'error': 'Resource Exhusted !'}), 401
#         elif response.status_code == 504:
#             return jsonify({'error': 'Service Temporarily unavilable !'}), 504
#         elif response.status_code == 500:
#             return jsonify({'error': 'Something went wrong. Please try again later !'}), 500
#         elif response.status_code == 404:
#             return jsonify({'error': 'Check the url.Page not found !'}), 404

#         response.raise_for_status()

#         response_json = response.json()
#         if 'candidates' in response_json and len(response_json['candidates']) > 0:
#             result = response_json['candidates'][0]['content']['parts'][0]['text']
#             filters = json.loads(result)
#             filters['prompt'] = query
#             result = json.dumps(filters, indent=2)
#         else:
#             result = {
#                 "action_intent": "search",
#                 "filters": {
#                     "category_name": "",
#                     "brand_name": "",
#                     "price_min": "",
#                     "price_max": "",
#                     "provider_name": "",
#                     "query_entity_type": "",
#                     "colour": "",
#                     "material": "",
#                     "pattern": "",
#                     "size": "",
#                     "gender": "",
#                     "sort_by": "",
#                     "numeric_clothing_size": "",
#                     "shoe_size": "",
#                     "neck_style": "",
#                     "occasion": "",
#                     "fit_type": "",
#                     "sleeve_length": "",
#                     "care_instructions": "",
#                     "sleeve_type": "",
#                     "weight": "",
#                     "memory_RAM": "",
#                     "storage": "",
#                     "battery_capacity": "",
#                     "seasons": "",
#                     "model_year": "",
#                     "cell_phone_features": "",
#                     "veg_type": "",
#                     "operating_system": "",
#                     "pocket_type": "",
#                     "special_features": "",
#                     "air_conditioner_type": "",
#                     "specialty_food_type": "",
#                     "diet_type": "",
#                     "condition": "",
#                     "craft_type": "",
#                     "connectivity_technology": "",
#                     "ingredient": "",
#                     "skin_tone": "",
#                     "skin_type": "",
#                     "finish": "",
#                     "health_concern": "",
#                     "health_benefit": "",
#                     "topping": "",
#                     "crust_type": "",
#                     "formulation": "",
#                     "hemline": "",
#                     "shape": "",
#                     "cuisine_type": ""
#                 },
#                 "prompt": query
#             }

#         return jsonify({'result': result})

#     except requests.RequestException as e:
#         app.logger.error(f"Request error occurred: {e}")
#         return jsonify({'error': 'Failed to connect to the external service'}), 500
#     except json.JSONDecodeError as e:
#         app.logger.error(f"JSON decode error: {e}")
#         return jsonify({'error': 'Failed to process JSON data'}), 500
#     except Exception as e:
#         app.logger.error(f"Unexpected error occurred: {e}")
#         return jsonify({'error': 'An unexpected error occurred'}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)


from flask import Flask, request, jsonify
from google.oauth2 import service_account
import vertexai
from vertexai.preview.generative_models import GenerativeModel

app = Flask(__name__)

SERVICE_ACCOUNT_FILE = './cartesian-service.json'
PROJECT_ID = '380777522230'
LOCATION = 'asia-south1'
ENDPOINT_ID = '5207080360961114112'

def init_vertexai():
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
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
