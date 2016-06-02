import requests
import json

payload = {
        'product_id': '1408850257',
        'website': 'amazon.in',
        'url': 'xyz',
        'email': 'vivekanand1101@gmail.com',
}

r = requests.post (
    "http://172.17.16.216:5001/home",
    json.dumps(payload),
    verify=False,
    headers={'Content-Type': 'application/json'}
)

print r.text
