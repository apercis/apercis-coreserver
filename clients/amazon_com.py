import requests
import json

payload = {
        'product_id': '0224602799',
        'website_name': 'amazonIN',
        'url': 'xyz'
}

r = requests.post (
    "http://127.0.0.1:5000",
    json.dumps(payload),
    headers={'Content-Type': 'application/json'}
)

print r.text
