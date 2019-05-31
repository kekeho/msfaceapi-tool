import requests
import json

with open('api_config.json', 'r') as f:
    api_conf = json.load(f)

SUBSCRIPTION_KEY = api_conf['subscription_key']
FACE_API_URL = api_conf['face_api_url']

headers = {
    'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
    'Content-type': 'application/octet-stream',
}

get_face_attributes = [
    'age',
    'gender',
    'headPose',
    'smile',
    'facialHair',
    'glasses',
    'emotion',
    'hair',
    'makeup',
    'occlusion',
    'accessories',
    'blur',
    'exposure',
    'noise'
]

params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'true',
    'returnFaceAttributes': ','.join(get_face_attributes),
}

with open('test.jpg', 'rb') as img:
    image = img.read()

response = requests.post(FACE_API_URL, params=params, headers=headers, data=image)

data = json.dumps(response.json())
print(data)
