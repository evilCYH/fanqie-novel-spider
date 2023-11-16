import pandas as pd
import requests
import random
import re
from ebooklib import epub
from time import sleep
from tqdm import tqdm
from bs4 import BeautifulSoup

def get_chapter_content(headers, path):
    novel_name = re.search(r'download\\(.*?)$', path).group(1)
    chapter_txt = f'{path}\{novel_name}.txt'
    chapter_csv = f'{path}\chapter_data.csv'
    chapter_data = pd.read_csv(chapter_csv)
    for index, row in chapter_data.iterrows():
        api_response = requests.get(row['Api'], headers=headers)
        # 解析 api 响应为 json 数据
        api_data = api_response.json()
        content_html = api_data['data']['content']

        soup = BeautifulSoup(content_html, 'html.parser')

        chapter_name = soup.find('header').text

        paragraphs = soup.find_all('p')
        chapter_content = ''
        # 遍历所有找到的 <p> 标签，并输出其文本内容
        for paragraph in paragraphs:
            line = '　　' + paragraph.text + '\n'
            chapter_content += line

        first_para = re.search(r'<p>(.*?)</p>', str(paragraphs[0])).group(1)
        if first_para != '':
            chapter_content = '　　\n' + chapter_content

        with open(chapter_txt, 'a', encoding='utf-8') as file:
            file.write(chapter_name + '\n')
            file.write(chapter_content)
            file.write('\n')
            file.write('\n')

        print(f"{row['Title']}  已经写入txt")

        rest_time = round(random.uniform(0.3, 1), 2)
        sleep(rest_time)



def create_epub(headers, path):
    novel_name = re.search(r'download\\(.*?)$', path).group(1)
    epub_name = f'{path}\{novel_name}.epub'
    chapter_csv = f'{path}\chapter_data.csv'
    chapter_data = pd.read_csv(chapter_csv)

    toc_items = []

    book = epub.EpubBook()
    book.set_cover("image.jpg", open(f'{path}\cover.jpg', 'rb').read())

    book.set_title(novel_name)
    book.set_language('zh-CN')

    for index, row in tqdm(chapter_data.iterrows(), desc="Downloading chapters", total=len(chapter_data)):
        retry_count = 1
        while retry_count < 4:  # 设置最大重试次数
            try:
                api_response = requests.get(row['Api'], headers=headers)
                api_data = api_response.json()

            except Exception as e:
                if retry_count == 1:
                    tqdm.write(f"错误：{e}")
                    tqdm.write(f"{row['Title']} 获取失败，正在尝试重试...")
                tqdm.write(f"第 ({retry_count}/3) 次重试获取章节内容")
                retry_count += 1  # 否则重试
                continue

            if "data" in api_data and "content" in api_data["data"]:
                content_html = api_data['data']['content']
                break  # 如果成功获取章节内容，跳出重试循环
            else:
                if retry_count == 1:
                    tqdm.write(f"{row['Title']} 获取失败，正在尝试重试...")
                tqdm.write(f"第 ({retry_count}/3) 次重试获取章节内容")
                retry_count += 1  # 否则重试

        if retry_count == 4:
            tqdm.write(f"无法获取章节内容: {row['Title']}，跳过。")
            continue  # 重试次数过多后，跳过当前章节

        soup = BeautifulSoup(content_html, 'html.parser')

        chapter_name = soup.find('header').text

        paragraphs = soup.find_all('p')
        chapter_content = ''

        # 添加章节标题到正文中
        chapter_content += f'<p style="font-family: 思源宋体; font-size: 24px; font-weight: bold;">{chapter_name}</p>'

        first_para = re.search(r'<p>(.*?)</p>', str(paragraphs[0])).group(1)
        if first_para != '':
            new_p_tag = soup.new_tag('p')
            paragraphs.insert(0, new_p_tag)

        for paragraph in paragraphs:
            line = '<p style="font-family: 微软雅黑">' + paragraph.text + '</p>'
            chapter_content += line

        # 创建章节
        epub_chapter = epub.EpubHtml(title=chapter_name, file_name=f'chapter_{index+1}.xhtml')
        epub_chapter.content = chapter_content

        # 添加章节到书籍
        book.add_item(epub_chapter)
        toc_items.append(epub.Link(f'chapter_{index+1}.xhtml', f"{row['Title']}", f'chapter{index+1}'))

        print(f"{row['Title']} 已添加到epub")

        rest_time = round(random.uniform(0.3,1),2)
        sleep(rest_time)

    book.toc = tuple(toc_items)

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # 生成epub文件
    epub.write_epub(epub_name, book)
