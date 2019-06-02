import requests
import json
import time
from PIL import Image
import io
from typing import List, Dict, ByteString


def server_error_validate(resp_json: Dict or List) -> (bool, int):
    """Check server error.
    Arg:
        resp_json (json dict, list): server response
    Return:
        when error occured: True, try_again_sec: int
        there is no error: False, -1
    """

    if type(resp_json) == dict and 'error' in resp_json.keys():
        try_again_sec = int(resp_json['error']['message'].split('Rate limit is exceeded. Try again in ')[-1].split(' seconds.')[0])
        return True, try_again_sec

    else:
        return False, -1


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

    def get(self, image_binary: ByteString, image_filename: str, auto_enlarge: bool = True) -> List[Face] or None:
        """Send image to Face API server, and get result json
        Args:
            image_binary: image (face included)
            image_filename: filename
            auto_enlarge:
                True: Send enlarged image (improve recognition rate)
                False: Send original image
        Return:
            Faces list
        """
        if auto_enlarge:
            image = Image.open(image_filename)
            enlarge_rate = 4200 / max(image.width, image.height)
            enlarged_image = image.resize(map(int, map(lambda x: x*enlarge_rate, (image.width, image.height))))
            fp = io.BytesIO()
            enlarged_image.save(fp, 'JPEG')
            image_binary = fp.getvalue()

        response = requests.post(
            self.endpoint_url, params=self.params, headers=self.headers, data=image_binary)
        resp_json = response.json()

        if resp_json != []:
            error, try_sec = server_error_validate(resp_json)
            if error:
                # Retry recursive 
                print(f'[Server error]({image_filename}): try after {try_sec}sec ago')
                time.sleep(try_sec + 1)
                return self.get(image_binary, image_filename)
            else:
                return [Face(resp_json[i], image_filename) for i in range(len(resp_json))]
        else:
            # can't recognize
            return None
