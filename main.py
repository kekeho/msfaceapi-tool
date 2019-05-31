import json
from lib.utils import Client

with open('api_config.json', 'r') as f:
    api_conf = json.load(f)

FACE_API_URL = api_conf['face_api_url']
SUBSCRIPTION_KEY = api_conf['subscription_key']

c = Client(FACE_API_URL, SUBSCRIPTION_KEY)

with open('test.jpg', 'rb') as img:
    image = img.read()
    result = c.get(image)
    print(result)
