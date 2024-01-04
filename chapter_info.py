import random
import sys
import requests
import re
import os
import csv
import json
from bs4 import BeautifulSoup
from time import sleep

def make_random_headers():
    # 获取打包后可执行文件的路径
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_path, "a.txt")
    with open(file_path, 'r') as file:
        user_agents = file.readlines()
    ua = random.choice(user_agents).strip()
    header = {
        'User-Agent': ua,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'TE': 'trailers'
    }
    return header

def get_novel_info(url):
    headers = make_random_headers()
    response = requests.get(url, headers=headers)
    # response.encoding = 'gbk'

    if response.status_code != 200:
        raise ValueError(f"网址未能访问，error code：{response.status_code}")

    # 转换为soup对象
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)

    # 获取html中的title
    long_name = soup.find('title').text

    # 从title中提取小说名字
    name_match = re.search(r'_(.*?)小说_', long_name)
    if name_match:
        novel_name = name_match.group(1)
        # print(f'==================== novel_name : {novel_name} ====================')
    else:
        raise ValueError("No title match found")

    # 相关文件夹
    global save_path

    # 检查download文件夹
    download_path = f'./download/'
    if not os.path.exists(download_path):
        print("download 文件夹未创建，开始创建")
        os.mkdir(download_path)
        print("download 文件夹已创建完毕")

    # 检查小说文件夹
    save_path = f'./download/{novel_name}'
    if not os.path.exists(save_path):
        print(f'{save_path} 文件夹未创建，开始创建')
        os.mkdir(save_path)
        print('文件夹已创建完毕')

    # 获取小说info的json
    novel_info = soup.find('script', type="application/ld+json").string
    parsed_info = json.loads(novel_info)

    # 获取img封面的url
    img_url = parsed_info['image'][0]

    img_response = requests.get(img_url, headers=headers)
    img = img_response.content

    # 保存图像到本地文件
    if os.path.exists(f'{save_path}/cover.jpg'):
        print('封面已存在, go on')
    else:
        with open(f"{save_path}/cover.jpg", "wb") as f:
            f.write(img)
            print('封面已保存完毕')

    # 获取每章的name、href
    chapter_title_all = soup.find_all('a', class_='chapter-item-title', target='_blank')
    chapter_list = []
    for chapter_title in chapter_title_all[1:]:
        chapter_name = chapter_title.get_text()
        chapter_href = 'https://fanqienovel.com' + chapter_title['href']
        chapter_id = re.search(r'\d+', chapter_title['href']).group()
        chapter_api = (f"https://novel.snssdk.com/api/novel/book/reader/full/v1/?device_platform=android&"
                       f"parent_enterfrom=novel_channel_search.tab.&aid=2329&platform_id=1&group_id={chapter_id}&item_id={chapter_id}")
        chapter_list.append([chapter_name, chapter_href, chapter_api])

    # 写入CSV文件
    csv_filename = f'{save_path}/chapter_data.csv'

    with open(csv_filename, 'w', newline='', encoding="utf_8_sig") as csv_file:
        csv_writer = csv.writer(csv_file)
        # 写入表头
        csv_writer.writerow(['Title', 'URL', 'Api'])
        # 写入数据
        csv_writer.writerows(chapter_list)

    print(f'章节数据已经写入 {save_path}/chapter_data.csv')

    return save_path

# # test
# if __name__ == '__main__':
#     url = 'https://fanqienovel.com/page/7299902479909522494'
#     headers = {
#         "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
#     }
#     get_novel_info(url, headers)