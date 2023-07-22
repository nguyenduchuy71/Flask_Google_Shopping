import os
import requests
from flask import Flask, request
from flask_caching import Cache
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
TIME_EXPIRATION = os.getenv("TIME_EXPIRATION", 10)
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
URL = 'https://realtime.oxylabs.io/v1/queries'

app = Flask(__name__)
cors = CORS(app)
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': f'redis://localhost:{REDIS_PORT}/0'})

@app.route('/', methods=['GET'])
@cache.cached(timeout=TIME_EXPIRATION)
def index():
    return '<b>This is server for getting product from google shopping!</b>'


@app.route('/get_product', methods=['POST'])
@cache.cached(timeout=TIME_EXPIRATION)
def get_product():
    try:
        data = request.json
        payload = {
            'source': 'google_shopping_search',
            'domain': 'com',
            'pages': 1,
            'parse': True,
            'context': [],
        }
        if data['nameProduct'] != '':
            payload['query'] = data['nameProduct']
        if data['pages'] != '':
            payload['pages'] = int(data['pages'])
        if data['sort'] != '':
            payload['context'].append(
                {'key': 'sort_by', 'value': data['sort']})
        if data['minPrice'] != '':
            payload['context'].append(
                {'key': 'min_price', 'value': data['minPrice']})
        if data['maxPrice'] != '':
            payload['context'].append(
                {'key': 'max_price', 'value': data['maxPrice']})
        response = requests.request(
            'POST',
            URL,
            auth=(USERNAME, PASSWORD),
            json=payload,
        )
        return {'status_code': 200, 'list_product': response.json()}
    except Exception as e:
        return {'status_code': 400, 'error': e}


@app.route('/get_product/<productId>', methods=['GET'])
@cache.cached(timeout=TIME_EXPIRATION)
def get_product_by_id(productId):
    try:
        payload = {
            'source': 'google_shopping_product',
            'domain': 'com',
            'query': str(productId),
            'parse': True,
        }
        response = requests.request(
            'POST',
            URL,
            auth=(USERNAME, PASSWORD),
            json=payload,
        )
        return {'status_code': 200, 'product': response.json()}
    except Exception as e:
        return {'status_code': 400, 'error': e}


if __name__ == '__main__':
    port = int(os.getenv('PORT', 3001))
    app.run(debug=False, host='0.0.0.0', port=port)
