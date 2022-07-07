import csv
import requests
import re
import json
import os
import pickle
import time

# 对应项在excel中的列下标
# 购买者姓名
INDEX_BUYER_NAME = 0
# 商品姓名
INDEX_ITEM_NAME = 1
# 商品地址（仅京东）
INDEX_ITEM_URL = 2
# 商品数量
INDEX_ITEM_NUM = 3;

SHOPPING_BASE_URL = 'https://cart.jd.com/gate.action?pid={0}&pcount={1}&ptype=1'

SAVED_FILE_NAME = 'remain_books.tmp'

CD = 1.0

def get_cookie():
    cookie = ''
    with open('./config.json') as f:
        cookie = json.load(f)['cookie']
    return cookie

def get_headers(cookie):
    headers = {
        'User=Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30',
        'Referer': 'https://www.jd.com/',
        'Cookie': cookie}
    return headers

def get_item_list():
    item_list = []
    if os.path.exists(SAVED_FILE_NAME):
        # load the books that are failed to put in the cart last time
        print(f'[LOG] saved book list found，loading...')
        item_list = pickle.load(open('./' + SAVED_FILE_NAME, 'rb'))
    else:
        print(f'[LOG] reading book list from books.csv...')
        csv_reader = csv.reader(open("./books.csv", encoding='UTF-8'))
        for i, item in enumerate(csv_reader):
            # skip the first row
            if (i == 0): 
                continue

            # skip empty and invalid entities
            if (len(item) == 0 or len(item[INDEX_BUYER_NAME]) == 0 or 
                len(item[INDEX_ITEM_NAME]) == 0 or 
                len(item[INDEX_ITEM_URL]) == 0):
                print(f'[LOG][{i+1}] Skipped empty entity.')
                continue

            # default 1 if the count is not filled.
            if not item[INDEX_ITEM_NUM]:
                item[INDEX_ITEM_NUM] = 1

            item_list.append(item)

        # pickle.dump(item_list, open('./' + SAVED_FILE_NAME, 'wb'))
    return item_list

def get_item_id(item):
    pattern = r'\d+'
    number_strings = re.findall(pattern, item[INDEX_ITEM_URL])
    if len(number_strings) < 1:
        print(f'[ERROR] getting {item[INDEX_BUYER_NAME]}\'s 《{item[INDEX_ITEM_NAME]}》 failed! The url: {item[INDEX_ITEM_URL]}')
        return None
    else:
        return number_strings[0]

def put_in_cart(book_list, cd):
    # load cookie from config.json
    cookie = get_cookie()
    if not cookie:
        print(f'Can\'t process without cookie. Please fill your JD cookie in config.json file.')
        return

    # set the headers
    headers = get_headers(cookie)

    success_list = []
    fail_list = []
    total_num = len(book_list)
    
    # put books from book_list into cart
    for i, item in enumerate(book_list):
        # print(f'{i}: {item}')
        book_id = get_item_id(item)
        book_num = item[INDEX_ITEM_NUM] if item[INDEX_ITEM_NUM] else 1

        shopping_url = SHOPPING_BASE_URL.format(book_id, book_num)
        content = requests.get(shopping_url, headers=headers)
        success_pattern = '商品已成功加入购物车'
        if success_pattern in content.text:
            success_list.append(item)
            print(f'[LOG][{i+1}/{total_num}] {item[INDEX_BUYER_NAME]}\'s <<{item[INDEX_ITEM_NAME]}>> is put into cart successfully.')
        else:
            print(f'[ERROR][{i+1}/{total_num}] {item[INDEX_BUYER_NAME]}\'s <<{item[INDEX_ITEM_NAME]}>> failed! Manual operation required: {item[INDEX_ITEM_URL]}')
            # DEBUG
            print(f'{content.text}')
            fail_list.append(item)
        
        # auto save per 50 books
        if len(fail_list) > 0 and (i+1) % 50 == 0:
            pickle.dump(fail_list, open('./' + SAVED_FILE_NAME, 'wb'))

        time.sleep(cd)

    return success_list, fail_list

def main():
    book_list = get_item_list()
    success_list, fail_list = put_in_cart(book_list, CD)
    
    if len(fail_list) > 0:
        pickle.dump(fail_list, open('./' + SAVED_FILE_NAME, 'wb'))
    
    print(f'[LOG] Mission completed.')
    print(f'[LOG] {len(success_list)} books are put in cart successfully.')
    print(f'[LOG] {len(fail_list)} books are failed and saved for the next process or add them manually:')
    for i, item in enumerate(fail_list):
        print(f'[LOG]{item[INDEX_BUYER_NAME]}\'s <<{item[INDEX_ITEM_NAME]}>> x {item[INDEX_ITEM_NUM]}: {item[INDEX_ITEM_URL]}')

def debug():
    pass


if __name__ == '__main__':
    main()
    # debug()