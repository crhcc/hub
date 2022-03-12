# -*- coding: utf-8 -*-
import base64
import requests,json
import time
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from Crypto.Util.Padding import pad

# 青龙安装依赖  pycryptodome

# 安卓用HttpCanary去微信小程序抓包，只能抓用户中心home_info_body的包。
# ios可用Thor去电信营业厅app抓包，Thor可抓所有包，可以PDD买账号下载。Stream无法抓包，其它抓包软件自测。

# 抓包数据填脚本里

# 手机号
config_list = [
   {"mobile": "19359263880", "food": True}
]
# 用户中心
# 抓包url   https://wapside.189.cn:9001/jt-sign/api/home/homeInfo
# home_info_body   {"para":"xx"}
home_info_body = {"para": "9619bb406db977fcc0cdfe7389702e63e4b27f59c98c0e82a35c35a64a20100fe0c37f36916dddd931556406e49b3d83366e08876b07ce9fe8482d97c4ead16227dd53bdd9292e85b8faa75790aeee5c19f3421517f53e1d00ca30af68a0ae26b3f2d609babbbf444a098faa0501bbbdf6cf6b5162a29c783ebfe3a5b37764fa3f2e3afe1adc5c7fc815757c28c2e21f4109bc325e33df8234d1c6a3fb929799377e5621791b3418ce08d7902ba57c075fcdc36c41dfdb620ac21943b55e915a8942bdcd822daa85eff19802abf31c67f005c95d6ca101c5e0afc72d0f065bb7f92a2d6e9aa40d7ceeb3b7671732a0c074701db910dfd1d4c6e3ecb96b23983b"}

# 喂宠物
# https://wapside.189.cn:9001/jt-sign/paradise/food
# food_body   {"para":"xx"}
food_body = {"para": "2940ba869a3e41da6e90dfba55c632b733abaca0850187f7b87e11c23b964d8e73421fa46b55b6baacfbbc1426991366679b2829f42b71ba792888ba3f2b0ebe3adf29d947304c4cce573ece43e627c5e46c5d07822eed9330fb77ebac2bf465c2ed188bed7c456b21f1f6b4cd736e75e720fc27ed6b7fdf581f6cdf3a9c8fc4"}


# 分享  
# https://dxhd.189.cn:7081/actcenter/v1/goldcoinuser/shareToGetCoin.do
# share_body = {
#     'activityId': 'telecomrecommend01',
#     'session': 'xxx'
# }
share_body = {}

# 云盘
# 'https://wapside.189.cn:9001/jt-sign/paradise/polymerize'
# cloud_body = {"para": "3c9ad2e3a7d1dad1139a53b8ba39899d43bc0b0d73589dfe2cc609281b4bd1688e7bbaa682a3eabfcb618b9d92c65a7191e1d876efcf366de248c84a72101e91276fb218010cf659171a31f399e0015de149359ae755f06ff4bc131cda6d4bc4ed256707af97f597c386c6673b36987602e20ee0b7e3d8cbbb83e304caa905a515f9a724d5e52a6cef37a71b8cc3da03b2f8fe4c3d3e7b746ef4583d1d92a60c4f2a73681a93c2b18f90d8ce09f5cfbfb8cc4857b6aac5a8d0407eca022e5025be4930cb1f94a50103bc30b36b7bab7d1efdf80351b53a0dbc5472f739cc9eab025653dfcb9c775554cccdbf5216d6fba1c2b8d39ab31622e1ff44ddeb6bf7c7"}
cloud_body = {"para": "3c9ad2e3a7d1dad1139a53b8ba39899d43bc0b0d73589dfe2cc609281b4bd1688e7bbaa682a3eabfcb618b9d92c65a7191e1d876efcf366de248c84a72101e91276fb218010cf659171a31f399e0015de149359ae755f06ff4bc131cda6d4bc4ed256707af97f597c386c6673b36987602e20ee0b7e3d8cbbb83e304caa905a515f9a724d5e52a6cef37a71b8cc3da03b2f8fe4c3d3e7b746ef4583d1d92a60c4f2a73681a93c2b18f90d8ce09f5cfbfb8cc4857b6aac5a8d0407eca022e5025be4930cb1f94a50103bc30b36b7bab7d1efdf80351b53a0dbc5472f739cc9eab025653dfcb9c775554cccdbf5216d6fba1c2b8d39ab31622e1ff44ddeb6bf7c7"}

# 种树
# 'https://wapside.189.cn:9001/jt-sign/paradise/polymerize'
# tree_body = {"para":"xx"}
tree_body = {"para": "3c9ad2e3a7d1dad1139a53b8ba39899d43bc0b0d73589dfe2cc609281b4bd1688e7bbaa682a3eabfcb618b9d92c65a7191e1d876efcf366de248c84a72101e91276fb218010cf659171a31f399e0015de149359ae755f06ff4bc131cda6d4bc4ed256707af97f597c386c6673b36987602e20ee0b7e3d8cbbb83e304caa905a515f9a724d5e52a6cef37a71b8cc3da03b2f8fe4c3d3e7b746ef4583d1d92a60c4f2a73681a93c2b18f90d8ce09f5cfbfb8cc4857b6aac5a8d0407eca022e5025be4930cb1f94a50103bc30b36b7bab7d1efdf80351b53a0dbc5472f739cc9eab025653dfcb9c775554cccdbf5216d6fba1c2b8d39ab31622e1ff44ddeb6bf7c7"}


msg = []

def telegram_bot(title, content):
    print("\n")
    title = title  # 改成你要的标题内容
    content = content  # 改成你要的正文内容
    bot_token = ''
    user_id = ''

    print("tg服务启动")
    url=f"https://api.telegram.org/bot{bot_token}/sendMessage"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'chat_id': str(user_id), 'text': f'{title}\n\n{content}', 'disable_web_page_preview': 'true'}
    proxies = None
    response = requests.post(url=url, headers=headers, params=payload, proxies=proxies).json()
    if response['ok']:
        print('推送成功！')
    else:
        print('推送失败！')


def encrypt(text):
    key = '34d7cb0bcdf07523'.encode('utf-8')

    cipher = AES.new(key, AES.MODE_ECB)
    pad_pkcs7 = pad(text.encode('utf-8'), AES.block_size, style='pkcs7')  # 选择pkcs7补全
    cipher_text = cipher.encrypt(pad_pkcs7)

    return b2a_hex(cipher_text)

def telecom_task(config):
    mobile = config['mobile']
    msg.append(mobile + " 开始执行任务...")
    h5_headers = get_h5_headers(mobile)
    # 获取用户中心
    home_info_ret = requests.post(url="https://wapside.189.cn:9001/jt-sign/api/home/homeInfo", json=home_info_body, headers=h5_headers).json()
    if home_info_ret['resoultMsg'] != "成功":
        msg.append(home_info_ret['resoultMsg'])
        return
    user_id = home_info_ret['data']['userInfo']['userThirdId']
    old_coin = home_info_ret['data']['userInfo']['totalCoin']

    # 签到
    t = time.time()
    time1 = int(round(t * 1000))
    body_json = {
        "phone": f"{mobile}",
        "date": time1,
        "signSource": "smlprgrm"
    }
    body_str = json.dumps(body_json)
    s = str(encrypt(body_str),'utf-8')
    sign_body = {
        "encode": s
    }

    sign_ret = requests.post(url="https://wapside.189.cn:9001/jt-sign/api/home/sign", json=sign_body,
                             headers=h5_headers).json()
    if sign_ret['data']['code'] == 1:
        msg.append("签到成功, 本次签到获得 " + str(sign_ret['data']['coin']) + " 豆")
    else:
        msg.append(sign_ret['data']['msg'])

    #share
    share(config)
    time.sleep(1)
    # 获取用户中心
    home_info_ret = requests.post(url="https://wapside.189.cn:9001/jt-sign/api/home/homeInfo", json=home_info_body,
                                  headers=h5_headers).json()
    new_coin = home_info_ret['data']['userInfo']['totalCoin']
    msg.append("领取完毕, 现有金豆: " + str(new_coin))
    msg.append("本次领取金豆: " + str(new_coin - old_coin))
    time.sleep(1)
    # 喂食
    food(config)

    msg.append("----------------------------------------------")

def food(config):
    if config['food']:
        mobile = config['mobile']
        msg.append(mobile + " 开始执行喂食...")
        while True:
            food_ret = requests.post(url="https://wapside.189.cn:9001/jt-sign/paradise/food", json=food_body,
                                     headers=get_h5_headers(mobile)).json()
            msg.append(food_ret['resoultMsg'])
            if food_ret['resoultCode'] != '0':
                break

#分享
def share(config):
    mobile = config['mobile']
    msg.append(mobile + "开始执行分享...")
    url = 'https://dxhd.189.cn:7081/actcenter/v1/goldcoinuser/shareToGetCoin.do'
    resp = requests.post(url=url,data=share_body,headers=get_h5_headers(mobile))
    print('share==============')
    print(resp)
    result = resp.text
    print(result)
    msg.append("分享" + result)

    cloud(mobile)
    time.sleep(2)
    tree(mobile)

# cloud
def cloud(mobile):
    msg.append(mobile + "访问云盘...")
    url='https://wapside.189.cn:9001/jt-sign/paradise/polymerize'
    resp = requests.post(url=url, json=cloud_body, headers=get_h5_headers(mobile))
    print('cloud=========')
    print(resp)
    result = resp.json()
    print(result)
    if result['resoultCode'] ==0:
        msg.append("云盘"+result['resoultMsg'])
    else:
        msg.append("云盘访问失败"+result['resoultMsg'])

# tree
def tree(mobile):
    msg.append(mobile + "种树...")
    url='https://wapside.189.cn:9001/jt-sign/paradise/polymerize'
    resp = requests.post(url=url, json=tree_body, headers=get_h5_headers(mobile))
    print('tree=========')
    print(resp)
    result = resp.json()
    print(result)
    if result['resoultCode'] ==0:
        msg.append("种树"+result['resoultMsg'])
    else:
        msg.append("种树访问失败"+result['resoultMsg'])


def get_h5_headers(mobile):
    base64_mobile = str(base64.b64encode(mobile[5:11].encode('utf-8')), 'utf-8').strip(r'=+') + "!#!" + str(
        base64.b64encode(mobile[0:5].encode('utf-8')), 'utf-8').strip(r'=+')
    return {"User-Agent": "CtClient;9.2.0;Android;10;MI 9;" + base64_mobile}


def format_msg():
    str = ''
    for item in msg:
        str += item + "\r\n"
    return str

def main_handler():
    for config in config_list:
        telecom_task(config)
    content = format_msg()

    print(content)
    telegram_bot('电信签到任务', content)
    return content

main_handler()
