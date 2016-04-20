import requests
import json

payload = {
        'product_id': 'xyz',
        'website': 'snapdeal.com',
        'url': 'http://www.snapdeal.com/product/samsung-galaxy-abc-8gb-4g/676860597612#bcrumbLabelId:175',
        'email': 'vivekanand1101@gmail.com',
}

r = requests.post(
        "http://172.19.13.41:5000/home",
        json.dumps(payload),
        headers = {
            'Content-Type': 'application/json'
        })

print r.text
