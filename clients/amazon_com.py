import requests
import json

payload = {
        'product_id': '0224602799',
        'website_name': 'amazonIN',
        'url': 'xyz'
}

r = requests.post (
    "http://172.19.13.41:5000/",
    json.dumps(payload),
    headers={'Content-Type': 'application/json'}
)

print r.text
