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

# 文本摘要： tencent
TENCENT_API_KEY = "AKIDlOnodEaidMs9D3e7MMTVQCm9K6h4D8oL"
TENCENT_API_SECRET = "NIzRffRzIMDpCKdiaFgtsiMmyxkJekbP"

XF_KEY_API_KEY = "523c2a7e9cf3f7e90cd3350193fdd22e"
XF_APP_ID = "4f59c1e9"


def text_abstraction_tencent(text):
    try:
        cred = credential.Credential(TENCENT_API_KEY, TENCENT_API_SECRET)

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

        resp = client.AutoSummarization(req)
        print(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)


# text_abstraction_tencent("中新经纬客户端4月4日电 中方于3月31日宣布对美国进口汽车及零部件暂停加征关税3个月，商务部发言人高峰4日在例行记者会上表示，3月5日，美方正式宣布再次推迟对中国输美产品加征关税税率提升至25%的期限。双方上述决定有助于为中美经贸磋商创造良好的氛围。发布会上，高峰表示，中美两国元首在G20阿根廷峰会期间举行会晤，就经贸问题达成重要共识。作为两国元首共识的一部分，美方对中国输美产品加征关税税率提升至25%的期限从2019年1月1日推迟到3月2日。之后，为推动磋商，中方宣布对原产于美国的汽车及零部件暂停加征关税3个月，截止日期为3月31日。3月5日，美方正式宣布再次推迟对中国输美产品加征关税税率提升至25%的期限，具体期限另行通知。3月31日，中国国务院关税税则委员会宣布延长对原产于美国的汽车及零部件暂停加征关税措施，截止日期另行通知。高峰指出，双方上述决定无疑有助于为中美经贸磋商创造良好的氛围。")


def keyword_xf(text):

    # 文本摘要：
    # https://cloud.tencent.com/document/product/271/35499
    # https://support.huaweicloud.com/api-nlp/nlp_03_0071.html
    # 关键词提取：
    # https://www.xfyun.cn/doc/nlp/keyword-extraction/API.html
    # https://support.huaweicloud.com/api-nlp/nlp_03_0084.html
    # https://cloud.tencent.com/document/api/271/35498

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
    result = result.read()
    print(result.decode('utf-8'))


keyword_xf("汉皇重色思倾国，御宇多年求不得。杨家有女初长成，养在深闺人未识。天生丽质难自弃，一朝选在君王侧。")
# https://ai.baidu.com/ai-doc/NLP/Gk6z52hu3