import json
import requests

################################################
app_id = "###"
app_secret = "###"
################################################

def img():
    url = 'https://www.dmoe.cc/random.php?return=json'
    img_data = requests.get(url).json()['imgurl']
    return img_data

# 获取token
def get_access_token():
    post_url = (
        f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}")
    try:
        access_token = requests.get(post_url).json()['access_token']
        print('[INFO]获取access_token成功!')
        return access_token
    except:
        print('[INFO]获取access_token失败请检查app_id和app_secret')


def get_openid(access_token):
    # 获取所有粉丝的openid
    next_openid = ''
    url_openid = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=%s' % (access_token, next_openid)
    ans = requests.get(url_openid)
    open_ids = json.loads(ans.content)['data']['openid']
    return open_ids

def sendmsg(access_token,user,img_url):
    url = f"https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={access_token}"
    body = {
        "touser": user,  # 用户的openid
        "msgtype": "news",  # 发送类型 图文消息
        "news": {
            "articles": [{
                "title": "标题",  # 标题
                "description": "正文",  # 内容描述
                "url": "跳转链接",  # 用户点击跳转的外链地址
                "picurl": "图片地址",  # 图片的地址
            }]
        }
    }
    # 请求
    data = bytes(json.dumps(body, ensure_ascii=False).encode('utf-8'))
    response = requests.post(url, data=data)
    res = response.json()
    if res['errcode']==0:
        print('[INFO]微信推文成功!')
    else:print(f'[INFO]微信推文失败{res}')

if __name__ == "__main__":
    # 获取access_token
    access_token = get_access_token()
    # 用户列表
    users = get_openid(access_token)
    # 图片
    img_data = img()
    for user in users:
        sendmsg(access_token, user, img_data)


