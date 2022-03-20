from util import get_ip_address

import urllib
import urllib.request

def drcom_login_dormitory(account, password):

    host = '172.30.255.42:801'
    referer = 'http://172.30.255.42/'
    login_url = 'http://172.30.255.42:801'

    print('Detecting IP address...')
    ip_address = ''
    try:
        ip_address = get_ip_address()
        print(f'IP address found: {ip_address}')
    except:
        print("Detect IP address failed.")
        exit(1)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39',
        'Connection': 'keep-alive',
        'Host': host,
        'Referer': referer
    }

    data_dict = {
        'callback': 'dr1003',
        'login_method': '1',
        'user_account': f',0,{account}',
        'user_password': password,
        'wlan_user_ip': ip_address,
        'wlan_user_mac': '000000000000',
        'jsVersion': '4.1.3',
        'terminal_type': '1',
        'v': '935',
    }

    data = bytes(urllib.parse.urlencode(data_dict), encoding='utf8')
    request = urllib.request.Request(
        url=f'{login_url}/eportal/portal/login?{urllib.parse.urlencode(data_dict)}',
        headers=headers, data=data, method='GET')

    response = urllib.request.urlopen(request)
    return response.reason


def drcom_login_lab(account, password):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39',
        'Connection': 'keep-alive',
        'Host': 'drcom.szu.edu.cn',
        'Origin': 'https://drcom.szu.edu.cn',
        'Referer': 'https://drcom.szu.edu.cn/a70.htm'
    }
    data = {
        'DDDDD': account,   # 账号
        'upass': password,   # 密码
        'R1': '0',
        'R2': '',
        'R6': '0',
        'para': '00',
        '0MKKey': '123456'
    }

    data = bytes(urllib.parse.urlencode(data), encoding='utf8')
    request = urllib.request.Request(
        url='https://drcom.szu.edu.cn/a70.htm',
        headers=headers, data=data, method='POST')
        
    response = urllib.request.urlopen(request)
    return response.reason


if __name__ == '__main__':
    drcom_login_dormitory()