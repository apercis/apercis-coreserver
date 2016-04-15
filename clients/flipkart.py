import requests
import json

payload = {
    'product_id': 'xyz',
    'website_name': 'flipkartcom',
    'url': 'http://www.flipkart.com/samsung-galaxy-j7/p/itmeafbfjhsydbpw?pid=MOBE93GWSMGZHFSK'
}

r = requests.post(
        "http://172.19.13.41:5000",
        json.dumps(payload),
        headers={'Content-Type': 'application/json'}
)

print r.text
