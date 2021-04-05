import requests
import re

def get_one_page(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None

def parse_one_page(html):
    pattern = re.compile("<dd>.*?broad-index")
    # TODO 正则表达式不对，继续修改，电子版书P162
    items = re.findall(pattern, html)
    print(items)

def main():
    url = 'https://maoyan.com/board/4'
    html = get_one_page(url)
    parse_one_page(html)

main()