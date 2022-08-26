import os
import random
import sys
from time import time, localtime
from datetime import datetime, date
import requests

# 获取token
def get_access_token():
    post_url = (
        f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}")
    access_token = requests.get(post_url).json()['access_token']
    print('[INFO]获取token成功!')
    return access_token

# 获取随机颜色
def get_color():
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)

# 重庆疫情
def cqyq():
    url = 'https://opendata.baidu.com/data/inner?tn=reserved_all_res_tn&resource_id=28565&query=上海新型肺炎最新动态'
    data = requests.get(url).json()['data'][0]['result']['items']
    data_print = '\n'
    for i in range(3):
        title = data[i]['eventDescription']
        # url = data[i]['eventUrl']
        data_print += title+"\n"
    print('[INFO]疫情模块加载正常')
    return data_print

# 获取温度
def get_weather(city_id):
    # 时间戳
    t = (int(round(time() * 1000)))
    headers = {
        "Referer": "http://www.weather.com.cn/",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    url = f"http://d1.weather.com.cn/weather_index/{city_id}.html?_={t}"
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"
    #print(response.text)
    response_data_0 = eval(response.text.split(";")[0].split("=")[-1])
    response_data_2 = eval(response.text.split(";")[2].split("=")[-1])
    response_data_3 = eval(response.text.split(";")[3].split("=")[-1])
    weatherinfo_0 = response_data_0["weatherinfo"]
    # 城市名称
    city_name = weatherinfo_0['city']
    # 最高气温
    max_wd = weatherinfo_0["temp"]
    # 最低气温
    min_wd = weatherinfo_0["tempn"]
    # 天气
    weather = weatherinfo_0["weather"]
    # 相对湿度
    shidu = response_data_2['SD']
    return city_name, weather, max_wd, min_wd,shidu

# 天行数据api
def tianapi(api_token):
    chp_url = f'http://api.tianapi.com/caihongpi/index?key={api_token}'
    zaxy_url = f'http://api.tianapi.com/zaoan/index?key={api_token}'
    jk_url = f'http://api.tianapi.com/healthtip/index?key={api_token}'
    chp_data = requests.get(chp_url).json()['newslist'][0]['content']
    zaxy_data = requests.get(zaxy_url).json()['newslist'][0]['content']
    jk_data = requests.get(jk_url).json()['newslist'][0]['content']
    return chp_data,zaxy_data,jk_data

# 推送信息
def send(template_id,to_user, access_token, city_name , weather, max_wd, min_wd,shidu, tips, yy,cqyq,chp):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    today = datetime.date(datetime(year=localtime().tm_year, month=localtime().tm_mon, day=localtime().tm_mday))
    week = week_list[today.isoweekday() % 7]
    # 特殊日期年月日
    year = config['to_time'][0]
    month = config['to_time'][1]
    day = config['to_time'][2]
    data = {
        "touser": to_user,
        "template_id": template_id,  # 模板id
        "url": config['url'],
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": "{} {}".format(today, week),
                "color": get_color()
            },
            "time": {
                "value": (datetime.today() - datetime(year,month,day)).days,
                "color": get_color()
            },
            "city": {
                "value": city_name,
                "color": get_color()
            },
            "weather": {
                "value": weather,
                "color": get_color()
            },
            "min_wd": {
                "value": min_wd,
                "color": get_color()
            },
            "max_wd": {
                "value": max_wd,
                "color": get_color()
            },
            "tips": {
                "value": tips,
                "color": get_color()
            },
            "shidu": {
                "value": shidu,
                "color": get_color()
            },
            "yy": {
                "value": yy,
                "color": get_color()
            },
            "yiqing": {
                "value": cqyq,
                "color": get_color()
            },
            "wh": {
                "value": chp,
                "color": get_color()
            },
        }
    }
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = requests.post(url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("[INFO]推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("[INFO]推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("[INFO]推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("[INFO]推送消息成功")
    else:
        print(response)


if __name__ == "__main__":
    try:
        with open("config.txt", encoding="utf-8") as f:
            config = eval(f.read())
    except FileNotFoundError:
        print("[INFO]请检查config.txt文件是否与程序位于同一路径")
        os.system("pause")
        sys.exit(1)
    except SyntaxError:
        print("[INFO]请检查配置文件格式是否正确")
        os.system("pause")
        sys.exit(1)
    #########################################################################################################
    users =config['users']
    template_id = config['template_id']
    city_id = config['city_id']
    app_id = config['app_id']
    app_secret = config['app_secret']
    api_token = config['api_token']
    ##########################################################################################################
    # 获取accessToken
    accessToken = get_access_token()
    # 天行数据api
    chp,zaxy,jk=tianapi(api_token)
    # 疫情信息
    cqyq=cqyq()
    # 公众号推送消息
    for user in users:
        # 传入省份和市获取天气信息
        city_name, weather, max_wd, min_wd,shidu = get_weather(city_id)
        send(template_id,user, accessToken, city_name, weather, max_wd, min_wd,shidu,jk, zaxy,cqyq,chp)
    os.system("pause")
    sys.exit(1)