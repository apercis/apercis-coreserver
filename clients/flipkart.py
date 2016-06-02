import requests
import json

payload = {
    'product_id': 'xyz',
    'website': 'flipkart.com',
    'url': 'http://www.flipkart.com/smart-dealz-ubon-ub-1085-designer-gaming-canal-earphone-microphone-iphone-samsung-htc-mi-super-bass-headphone-headphones/p/itmeexk4qfdqgugr?pid=ACCEEXK43UGW5WPC&al=Lk30qATLzjGzbnI%2FLIQHesldugMWZuE7sHPMhtl4IOrzzpSVAIs5cIbfXqmuuGt4GJ81eFD8hSY%3D&ref=L%3A2153276897080594144&srno=b_3',
    'email': 'vivekanand1101@gmail.com',
}

r = requests.post(
        "http://172.17.16.216:5000/home",
        json.dumps(payload),
        headers={'Content-Type': 'application/json'}
)

print r.text
