import http.client
import urllib.request, urllib.parse, urllib.error
import base64
import os
from pdb import set_trace
import math
import json
import pickle
import requests
from common_lib import *


file_name_counter = 0


def make_image_path(save_dir_path, url):

    global file_name_counter
    file_name_counter += 1
    image_file_name = 'img_{}'.format(str(file_name_counter))

    file_extension = os.path.splitext(url)[-1]
    if file_extension.lower() in ('.jpg', '.jpeg', '.gif', '.png', '.bmp'):
        full_path = os.path.join(save_dir_path, image_file_name + file_extension)
        return full_path
    else:
        raise ValueError('Not applicable file extension')


def download_image(url, timeout=10):
    response = requests.get(url, allow_redirects=True, timeout=timeout)
    if response.status_code != 200:
        error = Exception("HTTP status: " + response.status_code)
        raise error
    content_type = response.headers["content-type"]
    if 'image' not in content_type:
        error = Exception("Content-Type: " + content_type)
        raise error
    return response.content


def save_image(filename, image):
    with open(filename, "wb") as fout:
        fout.write(image)


def main():
    root_dir_path = './img'
    search_word = "喜多方ラーメン"
    save_dir_path = make_root_dir(root_dir_path, 'kitakata')

    # 必要な画像の総枚数
    total_image_number = 1500
    # 1トランザクションあたり、何枚取得するか？
    num_imgs_per_transaction = 150  # default 30, Max 150
    offset_count = math.floor(total_image_number / num_imgs_per_transaction)

    for offset in range(offset_count):

        url_list = []

        headers = {
            # Request headers
            'Content-Type': 'multipart/form-data',
            'Ocp-Apim-Subscription-Key': os.environ['BING_ACCESS_KEY'],
        }

        params = urllib.parse.urlencode({
            # Request parameters
            'q': search_word,
            'mkt': 'ja-JP',
            'count': num_imgs_per_transaction,
            'offset': offset * num_imgs_per_transaction
        })

        try:
            conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
            conn.request("GET", "/bing/v7.0/images/search?%s" % params, "", headers)
            response = conn.getresponse()
            results = response.read()

            save_res_path = os.path.join(save_dir_path, 'pickle_files')
            make_dir(save_res_path)
            with open(os.path.join(save_res_path, '{}.pickle'.format(offset)), mode='wb') as f:
                pickle.dump(results, f)
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
        else:
            decode_res = results.decode('utf-8')
            data = json.loads(decode_res)

            for values in data['value']:
                unquoted_url = urllib.parse.unquote(values['contentUrl'])
                url_list.append(unquoted_url)

        for url in url_list:
            try:
                image_path = make_image_path(save_dir_path, url)
                image = download_image(url)
                save_image(image_path, image)
                print('saved image... {}'.format(url))
            except KeyboardInterrupt:
                break
            except Exception as err:
                print("%s" % (err))


if __name__ == '__main__':
    main()


