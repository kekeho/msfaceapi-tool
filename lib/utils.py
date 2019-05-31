import requests
import json
from typing import List, Dict, ByteString


class Face(object):
    def __init__(self, json_info: Dict, image_filename: str):
        """
        Arg:
            json_info: result json from Face API
        """
        self.image_filename = image_filename
        self.json_data = json.dumps(json_info)
        self.json_dict = json_info
        self.face_id = json_info['faceId']
        # face attributes
        for k, v in json_info['faceAttributes'].items():
            self.__setattr__(k, v)
        # face landmarks
        for k, v in json_info['faceLandmarks'].items():
            self.__setattr__(k, list(v.values()))

        # face rectangle:
        __face_rect = json_info['faceRectangle']
        self.face_rectangle = [
            __face_rect['left'], __face_rect['top'],
            __face_rect['width'], __face_rect['height'],
        ]  # [x, y, width, height]


class Client(object):
    """Microsoft Face API Client"""

    def __init__(self, url: str, key: str):
        """Initialize
        Args:
            url: endpoint url
            key: access key
        """
        self.headers = {
            'Ocp-Apim-Subscription-Key': key,
            'Content-type': 'application/octet-stream',
        }
        self.get_face_attributes = [
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
        self.params = {
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'true',
            'returnFaceAttributes': ','.join(self.get_face_attributes),
        }
        self.endpoint_url = url

    def get(self, image_binary: ByteString, image_filename: str) -> List[Face]:
        """Send image to Face API server, and get result json
        Arg:
            image_binary: image (face included)
        Return:
            Faces list
        """
        response = requests.post(
            self.endpoint_url, params=self.params, headers=self.headers, data=image_binary)
        resp_json = response.json()

        return [Face(resp_json[i], image_filename) for i in range(len(resp_json))]
