import os
import requests
from flask import Flask, request
from flask_cors import CORS
from settings import USERNAME, PASSWORD

app = Flask(__name__)
cors = CORS(app)


@app.route('/', methods=['GET'])
def index():
    return '<b>This is server for getting product from google shopping!</b>'


@app.route('/get_product', methods=['POST'])
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
        print(f'data:{data}')
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
            'https://realtime.oxylabs.io/v1/queries',
            auth=(USERNAME, PASSWORD),
            json=payload,
        )
        return {'status_code': 200, 'list_product': response.json()}
    except Exception as e:
        return {'status_code': 400, 'error': e}


@app.route('/get_product/<productId>', methods=['GET'])
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
            'https://realtime.oxylabs.io/v1/queries',
            auth=(USERNAME, PASSWORD),
            json=payload,
        )
        return {'status_code': 200, 'product': response.json()}
    except Exception as e:
        return {'status_code': 400, 'error': e}


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5555))
    app.run(debug=False, host='0.0.0.0', port=port)
