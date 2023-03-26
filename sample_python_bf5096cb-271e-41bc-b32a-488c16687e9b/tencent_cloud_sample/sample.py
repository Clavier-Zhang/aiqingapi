# -*- encoding: utf-8 -*-
import base64
import hashlib
import urllib.parse
import urllib.request
import time
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.nlp.v20190408 import nlp_client, models
import requests

from ninterface import translate_json_to_record, show_record

TC_API_KEY = "AKIDlOnodEaidMs9D3e7MMTVQCm9K6h4D8oL"
TC_API_SECRET = "NIzRffRzIMDpCKdiaFgtsiMmyxkJekbP"

XF_KEY_API_KEY = "523c2a7e9cf3f7e90cd3350193fdd22e"
XF_APP_ID = "4f59c1e9"

BD_API_KEY = "e9aYf4di6t3YjOLeiLkhzFXu"
BD_SECRET_KEY = "LwfBelWkCreGfEuvqdmrGYpjCDHHMM6b"


def save_to_file(filename, text):
    text_file = open(f"{filename}.txt", "w")
    n = text_file.write(text)
    text_file.close()


class API:

    @staticmethod
    def text_abstraction_tc(text):
        try:
            cred = credential.Credential(TC_API_KEY, TC_API_SECRET)

            httpProfile = HttpProfile()
            httpProfile.endpoint = "nlp.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile)

            req = models.AutoSummarizationRequest()
            params = {
                "Text": text,
            }
            req.from_json_string(json.dumps(params))

            resp = client.AutoSummarization(req).Summary
            return resp

        except TencentCloudSDKException as err:
            print(err)

    @staticmethod
    def text_abstraction_bd(text):
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials",
                  "client_id": BD_API_KEY, "client_secret": BD_SECRET_KEY}
        token = str(requests.post(
            url, params=params).json().get("access_token"))

        url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/news_summary?charset=UTF-8&charset=&access_token=" + token
        url = f"https://aip.baidubce.com/rpc/2.0/nlp/v1/news_summary?access_token={token}&charset=UTF-8"

        payload = json.dumps({
            "content": text
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.request(
            "POST", url, headers=headers, data=payload).json()['summary']

        save_to_file("text_abstraction_bd", response)

        return response

    @staticmethod
    def keyword_xf(text):

        url = "https://ltpapi.xfyun.cn/v1/ke"

        body = urllib.parse.urlencode({'text': text}).encode('utf-8')
        param = {"type": "dependent"}
        x_param = base64.b64encode(json.dumps(
            param).replace(' ', '').encode('utf-8'))
        x_time = str(int(time.time()))
        x_checksum = hashlib.md5(XF_KEY_API_KEY.encode(
            'utf-8') + str(x_time).encode('utf-8') + x_param).hexdigest()
        x_header = {'X-Appid': XF_APP_ID,
                    'X-CurTime': x_time,
                    'X-Param': x_param,
                    'X-CheckSum': x_checksum}
        req = urllib.request.Request(url, body, x_header)
        result = urllib.request.urlopen(req)
        result = result.read().decode('utf-8')
        print(result)

        save_to_file("keyword_xf", result)
        return result

    @staticmethod
    def keyword_tc(text):
        try:
            cred = credential.Credential(TC_API_KEY, TC_API_SECRET)

            httpProfile = HttpProfile()
            httpProfile.endpoint = "nlp.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile

            client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile)

            req = models.KeywordsExtractionRequest()
            params = {
                "Text": text
            }
            req.from_json_string(json.dumps(params))

            resp = client.KeywordsExtraction(req).to_json_string()
            print(resp)
            save_to_file("keyword_tc", resp)
            return resp

        except TencentCloudSDKException as err:
            print(err)


def get_text_from_json():
    lines = translate_json_to_record('./ntemp.json')

    lines.sort(key=lambda line: int(line['start_time']))
    res = []
    for line in lines:
        if not res:
            res.append("说话人" + line['role'] + "说\"" + line['record'])
        elif line['role'] == res[-1][0]:
            res[-1] += line['record']
        else:
            res[-1] += "\""
            res.append("说话人" + line['role'] + "说\"" + line['record'])
    # for line in res:
    #     if line[-1] != '。':
    #         line += '。'
    return ''.join(res)


def generate_abstraction(text, api_method):
    res = []
    for i in range(len(text) // 2000):
        seg = text[i*2000: (i+1)*2000]
        print(len(seg))
        abstraction = api_method(seg)

        res.append(abstraction)
    return ''.join(res)


def generate_(text, api_method):
    res = []
    for i in range(len(text) // 2000):
        seg = text[i*2000: (i+1)*2000]
        print(len(seg))
        abstraction = api_method(seg)

        res.append(abstraction)
    return ''.join(res)


data = get_text_from_json()
print(len(data))

print(data)
save_to_file("data", data)


save_to_file("text_abstraction_tc", generate_abstraction(
    data, API.text_abstraction_tc))
save_to_file("text_abstraction_bd", generate_abstraction(
    data, API.text_abstraction_bd))


print('   ')
API.keyword_xf(data)
print('   ')
# data length cannot exceed 10000, since keyword detection cannot be separated
API.keyword_tc(data[:10000])
print('   ')
