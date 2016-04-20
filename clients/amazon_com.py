import requests
import json

payload = {
        'product_id': '0224602799',
        'website': 'amazon.in',
        'url': 'xyz',
        'email': 'vivekanand1101@gmail.com',
}

r = requests.post (
    "http://172.19.13.41:5000/home",
    json.dumps(payload),
    headers={'Content-Type': 'application/json'}
)

print r.text
