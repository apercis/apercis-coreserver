import requests
import json

payload = {
        'product_id': 'xyz',
        'website_name': 'snapdealcom',
        'url': 'http://www.snapdeal.com/product/intex-cloud-breeze-8gb-grey/671476050074#bcrumbLabelId:175'
}

r = requests.post(
        "http://127.0.0.1:5000",
        json.dumps(payload),
        headers = {
            'Content-Type': 'application/json'
        })

print r.text
