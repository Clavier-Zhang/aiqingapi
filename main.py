import requests


# https://cloud.tencent.com/document/product/271/35499


def call_summary_api(text):
    url = 'https://nlp.tencentcloudapi.com'

    body = {
        "Text": "选择一款笔记本，就是选择一种生活方式。对于成年人来说，选择笔记本最重要的还是CPU，毕竟打游戏的时间并没有那么多，所以除开少数行业之外更多还是CPU的比拼，毕竟干活的都是它。作为一个不喜欢把时间浪费在解决兼容性上的中年人，在购买笔记本这种是真要用来搞事情的产品时我还是更愿意选择英特尔。",
        "Length": 200
    }

    headers = {
        'Content-Type': 'application/json',
        'X-TC-Action': 'AutoSummarization'
    }

    response = requests.post(url, json=body, headers=headers)

    print(response.status_code)
    print(response.content)


call_summary_api("123")
