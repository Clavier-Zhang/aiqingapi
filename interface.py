# import requests
# import json

# def get_token(APPID, APP_Serect, url):

#     payload = ''
#     headers = {
#     'Content-Type': 'application/json',
#     }

#     response = requests.request("POST", url, headers=headers, data=payload)

#     result = json.loads(response.text)

#     access_ID = result['access_token']
    
#     return access_ID


# # 调用百度 API 的基础注册信息
# APPID = 'qh4biZkf2vtjtQrFmoU24Gcd'
# APP_Serect = 'RUaWUC1x9rmk0FhEce9yB4gKHVSzMepz'
# url = "https://aip.baidubce.com/oauth/2.0/token?client_id="+APPID+"&client_secret="+APP_Serect+"&grant_type=client_credentials"

# print(get_token(APPID, APP_Serect, url))


import base64
import hashlib
import hmac
import json
import os
import time
import requests
import urllib

lfasr_host = 'https://raasr.xfyun.cn/v2/api'
# 请求的接口名
api_upload = '/upload'
api_get_result = '/getResult'


class RequestApi(object):
    def __init__(self, appid, secret_key, upload_file_path, output_path):
        self.appid = appid
        self.secret_key = secret_key
        self.upload_file_path = upload_file_path
        self.output_path = output_path
        self.ts = str(int(time.time()))
        self.signa = self.get_signa()

    def get_signa(self):
        appid = self.appid
        secret_key = self.secret_key
        m2 = hashlib.md5()
        m2.update((appid + self.ts).encode('utf-8'))
        md5 = m2.hexdigest()
        md5 = bytes(md5, encoding='utf-8')
        # 以secret_key为key, 上面的md5为msg， 使用hashlib.sha1加密结果为signa
        signa = hmac.new(secret_key.encode('utf-8'), md5, hashlib.sha1).digest()
        signa = base64.b64encode(signa)
        signa = str(signa, 'utf-8')
        return signa


    def upload(self):
        print("上传部分：")
        upload_file_path = self.upload_file_path
        file_len = os.path.getsize(upload_file_path)
        file_name = os.path.basename(upload_file_path)

        param_dict = {}
        param_dict['appId'] = self.appid
        param_dict['signa'] = self.signa
        param_dict['ts'] = self.ts
        param_dict["fileSize"] = file_len
        param_dict["fileName"] = file_name
        param_dict["duration"] = "200"
        print("upload参数：", param_dict)
        data = open(upload_file_path, 'rb').read(file_len)

        response = requests.post(url =lfasr_host + api_upload+"?"+urllib.parse.urlencode(param_dict),
                                headers = {"Content-type":"application/json"},data=data)
        print("upload_url:",response.request.url)
        result = json.loads(response.text)
        print("upload resp:", result)
        return result


    def get_result(self):
        uploadresp = self.upload()
        orderId = uploadresp['content']['orderId']
        param_dict = {}
        param_dict['appId'] = self.appid
        param_dict['signa'] = self.signa
        param_dict['ts'] = self.ts
        param_dict['orderId'] = orderId
        param_dict['resultType'] = "transfer,predict"
        print("")
        print("查询部分：")
        print("get result参数：", param_dict)
        status = 3
        # 建议使用回调的方式查询结果，查询接口有请求频率限制
        while status == 3:
            response = requests.post(url=lfasr_host + api_get_result + "?" + urllib.parse.urlencode(param_dict),
                                     headers={"Content-type": "application/json"})
            # print("get_result_url:",response.request.url)
            result = json.loads(response.text)
            print(result)
            status = result['content']['orderInfo']['status']
            print("status=",status)
            if status == 4:
                break
            time.sleep(5)

        f = open(self.output_path, 'w', encoding='utf8')
        json.dump(result, f)
        print("get_result resp:",result)
        return result

def translate_wav_to_record(input_path, output_path):
    """
    描述：
        输入音频文件的文件 input_path，调用科大讯飞语音识别接口，将接口返回的信息保存为 json 文件存储到 output_path 中
    输入：
        input_path(str) : 音频文件的路径，音频文件需要保证为 wav 格式
        output_path(str) : 保存接口传回信息的 json 文件的路径
    输出:
        None
    """
    api = RequestApi(appid="50540b91",
                     secret_key="3f1b8b76ec9319eead58b05bff3f7b49",
                     upload_file_path=input_path,
                     output_path=output_path)
    

    api.get_result()




def translate_json_to_record(file_path):
    """
    描述：
        输入音频文件经过讯飞 API 进行语音识别后的保存的 json 文件路径 file_path，返回每一句话的信息列表
    输入：
        file_path(str) : 音频文件的路径，音频文件需要保证为 wav 格式
    输出:
        all_result(list) : 所有记录组成的列表，每个元素为 {'start_time' : 开始时间(ms), 'end_time' : 结束时间(ms), 'role' : 角色 ID(0:未识别，正整数代表识别角色), 'record' : 一段生成的文本}
    """
    f = open(file_path, 'r', encoding='utf8')
    result = json.load(f)
    sentences = json.loads(result['content']['orderResult'])['lattice'] # 获取所有经过平滑处理的语句
    all_result = []
    for i in range(len(sentences)):
        words = []
        s_obj = json.loads(sentences[i]['json_1best'])['st']

        start_time = s_obj['bg']
        end_time = s_obj['ed']
        label = s_obj['rl']
        content = s_obj['rt'][0]['ws']

        for j in range(len(content)):
            word = content[j]['cw'][0]['w'] # 获取一个识别出的单词
            words.append(word) # 将识别出的单词加入列表

        sentence = ''.join(words) # 将所有单词拼接在一起形成句子

        all_result.append({'start_time':start_time, 'end_time':end_time, 'role':label, 'record':sentence})

    return all_result


input_path = r"data/测试数据.wav"
output_path =  './output/tmp.json'
"""
translate_wav_to_record 调用科大讯飞接口
参考时间：
音频时长X（分钟）	参考返回时间Y（分钟）
X<10	Y<3
10<=X<30	3<=Y<6
30<=X<60	6<=Y<10
60<=X	10<=Y<20
"""
# translate_wav_to_record(input_path=input_path, output_path=output_path)
result = translate_json_to_record(file_path=output_path)
print(result.keys())
for i in range(len(result)): # 打印说话信息
    print(result[i]['record'])

