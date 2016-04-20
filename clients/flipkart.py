import requests
import json

payload = {
    'product_id': 'xyz',
    'website': 'flipkart.com',
    'url': 'http://www.flipkart.com/samsung-galaxy-j7/p/itmeafbfjhsydbpw?pid=MOBE93GWSMGZHFSK',
    'email': 'vivekanand1101@gmail.com',
}

r = requests.post(
        "http://172.19.13.41:5000/home",
        json.dumps(payload),
        headers={'Content-Type': 'application/json'}
)

print r.text
