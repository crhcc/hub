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
   {"mobile": "13159324621", "food": True}
]
# 用户中心
# 抓包url   https://wapside.189.cn:9001/jt-sign/api/home/homeInfo
# home_info_body   {"para":"xx"}
home_info_body = {"para": "45655e95620e86cd46ea10a1bd0054a256a226d10ea5a78a163ea06cd5c69d1fec231a1d0be3f9ee9ed5a260bccf832eb2535ecc085edffebcad3bf7fd32f33c0b483f5738b36ee8fabe4497cbb39fc7297611f575347e9988b751ce2a4e47f6e77e7b178af4098598a24247f47dd847faae1d636b00dcd2f93195b245f2b1aaa1ef583de1b3603c932412ad7f3dca50231b0fbcab7affb62470745fc8c81352bf6dbbbdc054daac5dc44addafd7bab5cd2bc039ff1c7bf9a9474ffff04afa77216b717245eaaf6ad496e90dfcefb3c78e7a17725fa2e9e6b397d7795b7eff51e211c8450b54aa6c838f60181b86b97253b5babaec9c1d81c16ac9c9b418fe84"}

# 喂宠物
# https://wapside.189.cn:9001/jt-sign/paradise/food
# food_body   {"para":"xx"}
food_body = {"para": "133b9a2783543065f07850e3361b55bca5f0019aa6bc4e6b5fc1a8c04c40d5d8dda3d629ee14750bf54404117624686451b61fe009081c7ce17ea1618b1e302df16f012183bf6157331f1363dbfd7bd1d8a87ec4007ccb9a93a6e22a958706b47cb2dd5ba75b1423f2b8a8c57600f65ae114686438c06989000c961967e1274e"}


# 分享  
# https://dxhd.189.cn:7081/actcenter/v1/goldcoinuser/shareToGetCoin.do
# share_body = {
#     'activityId': 'telecomrecommend01',
#     'session': 'xxx'
# }
share_body = {
'activityId': 'telecomrecommend01',
'session': '2022031213552771776fda366eba54e31bc6a363155a22409'
}

# 云盘
# 'https://wapside.189.cn:9001/jt-sign/paradise/polymerize'
# cloud_body = {"para":"xx"}
cloud_body = {"para": "acb89a33795c0f78d3a27114ba574792df172644ff608edbffc954e3c7c3f8be632a88fd66656278204ce9b747d89e74798d95d7bab10d894e233c967200d497b8f016a760389f515959642d6789b8f06a72b23b7bc9c358749b6739b6ea887e5f71e3ecf7a584a95cae70768226eaf275383138d603a60a5a0cb37e988b93a741341cbc303c3c2b264566935d8b65d453d2393daf731f268da0c8ca9dd4ae1e148e0205f48d32dc85fc0c54fb901a4ddfc665658c32b1808de2f97ec8aaa31f80684c3d505ba469289499d109ddee00162796e9ea51b9307394f3c31366ffaae356ffe17570899c36f810ec6768180142e270120e8f86c7bcbf110d41831b18"}

# 种树
# 'https://wapside.189.cn:9001/jt-sign/paradise/polymerize'
# tree_body = {"para":"xx"}
tree_body = {"para": "acb89a33795c0f78d3a27114ba574792df172644ff608edbffc954e3c7c3f8be632a88fd66656278204ce9b747d89e74798d95d7bab10d894e233c967200d497b8f016a760389f515959642d6789b8f06a72b23b7bc9c358749b6739b6ea887e5f71e3ecf7a584a95cae70768226eaf275383138d603a60a5a0cb37e988b93a741341cbc303c3c2b264566935d8b65d453d2393daf731f268da0c8ca9dd4ae1e148e0205f48d32dc85fc0c54fb901a4ddfc665658c32b1808de2f97ec8aaa31f80684c3d505ba469289499d109ddee00162796e9ea51b9307394f3c31366ffaae356ffe17570899c36f810ec6768180142e270120e8f86c7bcbf110d41831b18"}


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
