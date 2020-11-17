import os
import pickle
import re
import time
from urllib import parse

import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://bmcbioinformatics.biomedcentral.com'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51 '
}


def main():
    search_keyword = ''
    while not search_keyword:
        search_keyword = input('what u want?')
    volume = input('date?')
    if volume:
        volume = int(volume) - 1999
    is_download = input('Download PDF file?y/[n]')
    is_download = True if is_download == 'y' else False
    is_markdown = input('Export paper list to Markdown?y/[n]')
    is_markdown = True if is_markdown == 'y' else False
    is_csv = input('Export paper list to CSV?y/[n]')
    is_csv = True if is_csv == 'y' else False

    save_file_name = 'saved_articles_{}_{}.pkl'.format(search_keyword, volume)
    if os.path.exists(save_file_name):
        print('Found exist file, loading...')
        with open(save_file_name, 'rb') as f:
            article_list = pickle.load(f)
    else:
        print('Not found file, begin clawing...')
        params = {
            'tab': 'keyword',
            'searchType': 'journalSearch',
            'query': search_keyword,
            'page': 1,
            'volume': volume,
        }

        url = BASE_URL + '/articles' + '?' + parse.urlencode(params)

        # get the page num
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'lxml')
        pages = int(
            soup.find('p', class_='u-text-sm u-reset-margin').get_text().split()[-1])
        print('Get Total Pages: {}'.format(pages))

        article_list = []
        count = 1
        for page in range(1, pages + 1):
            print('Getting page {}...'.format(page))
            # response = requests.get(url + '&page=' + str(page))
            params['page'] = page
            url = BASE_URL + '/articles' + '?' + parse.urlencode(params)
            response = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(response.text, 'lxml')

            articles = soup.find_all('article', class_='c-listing')
            for i, article in enumerate(articles):
                title = article.h3.get_text(strip=True)
                abstract = article.find(
                    'p', class_='c-listing__text').get_text(strip=True)
                author = article.find(
                    'p', class_='c-listing__authors u-mb-0').contents[1].split(',')[0]
                url = article.h3.a['href']
                url = BASE_URL + url
                journal = article.find(
                    'div', class_='c-listing__text c-listing__text--light').p.get_text().split('\n')[2]
                date = article.find(
                    'div', class_='c-listing__text c-listing__text--light').p.get_text().split('\n')[3].strip()

                pdf = article.find(
                    'ul', class_='c-listing__view-options').find_all('li')[1].a['href']
                pdf = BASE_URL + pdf

                article_list.append({
                    'id': count,
                    'title': title,
                    'abstract': abstract,
                    'date': date,
                    'author': author,
                    'journal': journal,
                    'url': url,
                    'pdf': pdf,
                })
                count += 1
            # cd = random.uniform(1, 3)
            # time.sleep(cd)

        with open(save_file_name, 'wb') as f:
            pickle.dump(article_list, f)
            print('Result saved.')

    print('Got result: {}'.format(len(article_list)))
    if is_download:
        download_from_list(article_list)

    if is_markdown:
        export_to_md(article_list)

    if is_csv:
        export_to_csv(article_list)


def download_from_list(article_list):
    save_file_name = 'download'
    if not os.path.exists(save_file_name):
        os.mkdir(save_file_name)

    base_path = os.path.join(os.getcwd(), save_file_name)

    for article in article_list:
        # -年限-作者-会议-论文名称-

        folder_name = '--'.join([
            '',
            article['date'],
            article['author'],
            article['journal'][:3],
            re.sub(r':', '', article['title']),
        ])

        # path = os.path.join(base_path, folder_name)
        # if not os.path.exists(path):
        #     os.mkdir(path)
        # file = os.path.join(path, article['pdf'].split('/')[-1]) + '.pdf'
        file = os.path.join(base_path, folder_name)
        file = ''.join(file.split('/'))
        file = file[:255] + '.pdf'

        if not os.path.exists(file):
            with open(file, 'wb') as f:
                response = requests.get(article['pdf'], headers=HEADERS)
                f.write(response.content)

        time.sleep(5)


def export_to_md(article_list):
    save_file_name = 'output.md'

    from collections import defaultdict
    dic = defaultdict(list)
    for article in article_list:
        dic[article['date']].append(article)

    lines = []
    for date in sorted(dic.keys(), reverse=True):
        line = '## ' + date + '\n'
        lines.append(line)

        for article in dic[date]:
            line = '--'.join([
                '',
                article['date'],
                article['author'],
                article['journal'][:3],
                '**' + article['title'] + '**',
                '',
            ])
            line += ' [PDF]({})'.format(article['pdf'])
            line = '* ' + line + '\n'
            lines.append(line)

    with open(save_file_name, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line)


def export_to_csv(article_list):
    import csv
    save_file_name = 'output.csv'
    row = ['id', 'date', 'author', 'journal', 'title', 'url', 'pdf']
    with open(save_file_name, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=row)
        writer.writeheader()
        writer.writerows(article_list)


if __name__ == '__main__':
    main()
