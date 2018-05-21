import requests
import requests_oauthlib
import json
import math
import os
import urllib.request
from urllib.parse import urlparse
from common_lib import *
from pdb import set_trace

# 保存先ディレクトリの作成
directory = make_root_dir("./img", "kitakata")
# twitter APIのURL
url = "https://api.twitter.com/1.1/search/tweets.json"

# parameters
query = "喜多方ラーメン"
lang = "ja"
result_type = "recent"  # 最新のツイートを取得
count = 100  # 1回あたりの最大取得ツイート数（最大100）
max_id = ''

total_count = 10000 # 取得ツイートのトータル
offset = math.floor(total_count/count) # ループ回数

# oauthの設定
consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_secret = os.environ['ACCESS_SECRET']
oauth = requests_oauthlib.OAuth1(consumer_key,consumer_secret,access_token,access_secret)

for i in range(offset):
    params = {'q':query,'lang':lang,'result_type':result_type,'count':count,'max_id':max_id}
    r = requests.get(url=url,params=params,auth=oauth)
    json_data = r.json()
    print(json_data)
    for data in json_data['statuses']:
        # 最後のidを格納
        max_id = str(data['id']-1)
        if 'media' not in data['entities']:
            continue
        else:
            for media in data['entities']['media']:
                if media['type'] == 'photo':
                    image_url = media['media_url']
                    try:
                        save_image(image_url, directory)
                    except Exception as e:
                        print("failed to download image at {}".format(image_url))
                        print(e)
                        continue