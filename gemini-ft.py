
from flask import Flask, request, jsonify
from google.oauth2 import service_account
import vertexai
import os
from vertexai.preview.generative_models import GenerativeModel
import json

app = Flask(__name__)

PROJECT_ID = '380777522230'
LOCATION = 'asia-south1'
ENDPOINT_ID = '7749503088100114432'


def init_vertexai():
    credentials_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    if credentials_json:
        credentials_dict = json.loads(credentials_json)
        credentials = service_account.Credentials.from_service_account_info(credentials_dict)
    
    vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=credentials)
    
    model_endpoint = f'projects/{PROJECT_ID}/locations/{LOCATION}/endpoints/{ENDPOINT_ID}'
    model = GenerativeModel(model_endpoint)

    return model

model = init_vertexai()

@app.route('/intent', methods=['POST'])
def process_query():
    try:
        system_instruction = '''You are an Indian eCommerce assistant tasked with extracting key-value pairs in JSON format from a given query input text for the Plotch-Cartesian eCommerce platform.The final result should be presented in pure English, preserving the meaning of the input without altering it. *** Input Query *** : '''
        
        data = request.json
        query = data.get('query', '')

        if not query:
            return jsonify({'error': 'No query provided'}), 400

        prompt=system_instruction+query
        response = model.generate_content(prompt)

        result = response.text

        return jsonify({'result': result})

    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
