import requests
import json

payload = {
        'product_id': 'xyz',
        'website': 'snapdeal.com',
        'url': 'http://www.snapdeal.com/product/intex-cloud-breeze-8gb-grey/671476050074#bcrumbLabelId:175',
        'email': 'vivekanand1101@gmail.com',
}

r = requests.post(
        "http://172.19.13.41:5000/home",
        json.dumps(payload),
        headers = {
            'Content-Type': 'application/json'
        })

print r.text
