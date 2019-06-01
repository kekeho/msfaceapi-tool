import json
import argparse
import glob
import os
from concurrent.futures import ThreadPoolExecutor
import lib.utils
import re
from typing import List


with open('api_config.json', 'r') as f:
        api_conf = json.load(f)

FACE_API_URL = api_conf['face_api_url']
SUBSCRIPTION_KEY = api_conf['subscription_key']
c = lib.utils.Client(FACE_API_URL, SUBSCRIPTION_KEY)


def __target(image_filename) -> List[lib.utils.Face]:
    with open(image_filename, 'rb') as img:
        image = img.read()
        result = c.get(image, image_filename)
        return image_filename, result


def main():
    parser = argparse.ArgumentParser(prog='mface', description='Microsoft Face API commandline tool')
    parser.add_argument('dir' ,help="images dir")
    parser.add_argument('-f', '--format', choices=['json'], default='json',help='Result data format')
    parser.add_argument('-s', '--save', default='mface_result', help='save filename')
    args = parser.parse_args()

    executer = ThreadPoolExecutor(max_workers=10)
    image_list = [os.path.abspath(x) for x in glob.glob(os.path.join(args.dir, '*')) if x.split('.')[-1] in ['png', 'jpg', 'jpeg']]

    result = list(executer.map(__target, image_list))
    
    # save json
    json_dict = []
    for filename, image in result:
        if image != None:
            print(f'{filename}: {len(image)}')
            json_dict.append([filename, [f.json_dict for f in image]])
        else:
            print(f'Skip {filename}: no face')
    
    with open(args.save, 'w') as save:
        save.write(json.dumps(json_dict, indent=4, separators=(',', ':', )))


if __name__ == "__main__":
    main()