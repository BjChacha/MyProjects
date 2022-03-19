import os
import re
from urllib import parse, request
import sys
import time

HOST = '172.30.255.42:801'
REFERER = 'http://172.30.255.42/'
LOGIN_URL = 'http://172.30.255.42:801'

DEFAULT_ACCOUNT = '381393'
DEFAULT_PASSWORD = '136135'
DEFAULT_IP = '172.29.151.226'

def main():
    if len(sys.argv) != 3:
        print("No account detect, using default..")
        account = DEFAULT_ACCOUNT
        password = DEFAULT_PASSWORD
    else:
        account = sys.argv[1]
        password = sys.argv[2]

    print('Detecting IP address...')
    ip_address = ''
    try:
        ipconfig = os.popen('chcp 65001&&ipconfig').read()
        ip_address = re.findall('IPv4 Address.*?: (.*?)\n', ipconfig)[0]
        print(f'IP address found: {ip_address}')
    except:
        print("Detect IP address failed.")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39',
        'Connection': 'keep-alive',
        'Host': HOST,
        'Referer': REFERER
    }

    data_dict = {
        'callback': 'dr1003',
        'login_method': '1',
        'user_account': f',0,{account}',
        'user_password': password,
        'wlan_user_ip': ip_address,
        # 'wlan_user_ipv6': '',
        'wlan_user_mac': '000000000000',
        # 'wlan_ac_ip': '',
        # 'wlan_ac_name': '',
        'jsVersion': '4.1.3',
        'terminal_type': '1',
        # 'lang': 'zh-cn',
        'v': '935',
        # 'lang': 'zh',
    }
    data = bytes(parse.urlencode(data_dict), encoding='utf8')

    r = request.Request(
        url=f'{LOGIN_URL}/eportal/portal/login?{parse.urlencode(data_dict)}',
        headers=headers, data=data, method='GET')

    response = request.urlopen(r)
    # print(response.read().decode('gb2312'))
    print(response.reason)



if __name__ == '__main__':
    main()