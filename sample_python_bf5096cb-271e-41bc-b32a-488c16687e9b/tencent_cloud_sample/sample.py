# -*- encoding: utf-8 -*-
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.nlp.v20190408 import nlp_client, models
try:
    # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
    # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
    # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
    cred = credential.Credential("AKIDlOnodEaidMs9D3e7MMTVQCm9K6h4D8oL", "NIzRffRzIMDpCKdiaFgtsiMmyxkJekbP")
    # 实例化一个http选项，可选的，没有特殊需求可以跳过
    httpProfile = HttpProfile()
    httpProfile.endpoint = "nlp.tencentcloudapi.com"

    # 实例化一个client选项，可选的，没有特殊需求可以跳过
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    # 实例化要请求产品的client对象,clientProfile是可选的
    client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile)

    # 实例化一个请求对象,每个接口都会对应一个request对象
    req = models.AutoSummarizationRequest()
    params = {
        "Text": "中新经纬客户端4月4日电 中方于3月31日宣布对美国进口汽车及零部件暂停加征关税3个月，商务部发言人高峰4日在例行记者会上表示，3月5日，美方正式宣布再次推迟对中国输美产品加征关税税率提升至25%的期限。双方上述决定有助于为中美经贸磋商创造良好的氛围。发布会上，高峰表示，中美两国元首在G20阿根廷峰会期间举行会晤，就经贸问题达成重要共识。作为两国元首共识的一部分，美方对中国输美产品加征关税税率提升至25%的期限从2019年1月1日推迟到3月2日。之后，为推动磋商，中方宣布对原产于美国的汽车及零部件暂停加征关税3个月，截止日期为3月31日。3月5日，美方正式宣布再次推迟对中国输美产品加征关税税率提升至25%的期限，具体期限另行通知。3月31日，中国国务院关税税则委员会宣布延长对原产于美国的汽车及零部件暂停加征关税措施，截止日期另行通知。高峰指出，双方上述决定无疑有助于为中美经贸磋商创造良好的氛围。",
        "Length": 200
    }
    req.from_json_string(json.dumps(params))

    # 返回的resp是一个AutoSummarizationResponse的实例，与请求对象对应
    resp = client.AutoSummarization(req)
    # 输出json格式的字符串回包
    print(resp.to_json_string())

except TencentCloudSDKException as err:
    print(err)
