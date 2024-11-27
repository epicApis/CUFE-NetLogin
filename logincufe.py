# 在使用前，请先安装requests库，并确保你的网络连接到校园网
# 注意修改TERMINAL_USERNAME和TERMINAL_PASSWORD为你的学号和密码
from time import sleep, time
from requests import get
from json import loads
from re import search
from urllib.parse import quote_plus
from datetime import datetime, timedelta

TERMINAL_USERNAME = '2023311152'   # 你的学号
TERMINAL_PASSWORD = '1234567890'   # 你的密码
# 把用户名和密码转换为URL编码
URLENCODE_USERNAME = quote_plus(TERMINAL_USERNAME)
URLENCODE_PASSWORD = quote_plus(TERMINAL_PASSWORD)

MAX_TIMEOUT = 10  # 最大超时时间，单位秒
HINT_TIMEOUT = 5  # 提示超时时间，单位秒
TRY_INTERVAL = 0.5  # 尝试间隔，单位秒


class Url:
    def __init__(self, url, name):
        self.url = url
        self.name = name
        self.attempts = 0
        self.success = False


# 虽然理论上可以只从你所使用的校园网中获取，但是这里为了方便，直接全登录一遍
urls = [
    Url(f'http://10.2.193.1/drcom/login?callback=dr1003&DDDDD={URLENCODE_USERNAME}%40cufe&upass=' +
        f'{URLENCODE_PASSWORD}&0MKKey=123456', '学院南路无线网（10.2.193.1）'),
    Url(f'http://10.13.13.2/drcom/login?callback=dr1003&DDDDD={URLENCODE_USERNAME}&upass=' +
        f'{URLENCODE_PASSWORD}&0MKKey=123456', '沙河校区有线网（10.13.13.2）'),
    Url(f'http://10.200.0.5/drcom/login?callback=dr1003&DDDDD={URLENCODE_USERNAME}&upass=' +
        f'{URLENCODE_PASSWORD}&0MKKey=123456', '沙河校区无线网（10.200.0.5）'),
    Url(f'http://192.168.31.2/drcom/login?callback=dr1003&DDDDD={URLENCODE_USERNAME}&upass=' +
        f'{URLENCODE_PASSWORD}&0MKKey=123456', '学院南路有线网（192.168.31.2）')
]
remain_count = len(urls)
user_ip = None

start_time = time()
url_index = 0
hinted = False
while remain_count > 0:
    if not hinted and time() - start_time > HINT_TIMEOUT:
        print('仍在尝试……')
        if remain_count == len(urls):
            print('请检查是否连接到校园网，以及用户名和密码拼写')
        hinted = True
    if time() - start_time > MAX_TIMEOUT:
        break
    url_index = (url_index + 1) % len(urls)  # 循环尝试
    if urls[url_index].success:
        continue
    urls[url_index].attempts += 1
    response = get(urls[url_index].url)
    print(f'第{urls[url_index].attempts}次尝试登录 {urls[url_index].name}', end=' ')
    match = search(r'dr1003\((\{.*?\})\)', response.text)  # 匹配返回的json数据
    if not match:
        print('失败')
        continue
    json_data = loads(match.group(1))  # 解析json数据
    if response.status_code == 200 and json_data and json_data.get('result', 0) == 1:
        print('成功')
        user_ip = json_data.get('v46ip', None)
        urls[url_index].success = True
        remain_count -= 1
    else:
        print('失败')
    if remain_count > 0:
        sleep(TRY_INTERVAL)

if remain_count == len(urls):
    print('所有尝试均失败，请检查网络连接或用户名和密码拼写')
    exit(1)
elif remain_count > 0:
    print('部分尝试失败，但若能获取流量信息也算成功')
if not user_ip:
    print('未获取到IP地址，无法获取信息')
    exit(1)

sta_urls = [
    'http://10.2.193.1:801/eportal/portal/custom/userInfo?callback=dr1002&account=' +
    f'{URLENCODE_USERNAME}&ip={user_ip}',
    'http://10.13.13.2:801/eportal/portal/custom/userInfo?callback=dr1002&account=' +
    f'{URLENCODE_USERNAME}&ip={user_ip}',
    'http://10.200.0.5:801/eportal/portal/custom/userInfo?callback=dr1002&account=' +
    f'{URLENCODE_USERNAME}&ip={user_ip}',
    'http://192.168.31.2:801/eportal/portal/custom/userInfo?callback=dr1002&account=' +
    f'{URLENCODE_USERNAME}&ip={user_ip}'
]

sta_gotten = False
start_time = time()
sta_index = 3
attempts = 0
hinted = False
while not sta_gotten:
    if not hinted and time() - start_time > HINT_TIMEOUT:
        print('仍在尝试获取用户信息……')
        hinted = True
    if time() - start_time > MAX_TIMEOUT:
        print('获取信息超时，请稍后再试')
        break
    sta_index = (sta_index + 1) % len(sta_urls)
    attempts += 1
    response = get(sta_urls[sta_index])
    print(f'第{attempts}次尝试获取用户信息', end=' ')
    match = search(r'dr1002\((\{.*?\})\)', response.text)
    if not match:
        print('失败')
        continue
    json_data: dict = loads(match.group(1))
    if not json_data:
        print('失败')
        continue
    user_data: dict = json_data.get('user_data', None)
    if response.status_code == 200 and user_data:
        print('成功')
        user_totalflow = user_data.get('totalflow', 0)  # 注意解析后的数据类型
        user_leftflow = user_data.get('leftflow', 0)
        user_leftmoney = user_data.get('leftmoney', 0)
        user_packname = user_data.get('defaultname', '')
        print(f"用户编号: {TERMINAL_USERNAME}")
        print(f"登录IP: {user_ip}")
        if user_totalflow is not None:
            if user_totalflow > 1024:
                print(f"已用流量: {user_totalflow / 1024:.2f} GB")
            else:
                print(f"已用流量: {user_totalflow} MB")
        if user_leftflow is not None:
            if user_leftflow > 1024:
                print(f"剩余（不限速）流量: {user_leftflow / 1024:.2f} GB")
            else:
                print(f"剩余（不限速）流量: {user_leftflow} MB")
        print(f"剩余金额: {user_leftmoney}")
        print(f"套餐名称: {user_packname}")
        today = datetime.now()
        end_of_month = datetime(
            today.year, today.month + 1, 1) - timedelta(days=1)
        days_remaining = (end_of_month - today).days
        if days_remaining <= 2 and user_leftmoney is not None and user_leftmoney < 10:
            print("提示: 离月末不到2天，余额小于10元，请注意及时充值。")
        sta_gotten = True
    else:
        print('失败')
        sleep(TRY_INTERVAL)
# 该版本只保留了基础的登录和获取信息功能，并未实现自动（维持）登录和自动获取信息
