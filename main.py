import os
import chapter_info as info
import chapter_content as content
import re

def is_valid_url(url):
    # 正则表达式匹配 https://fanqienovel.com/page/ 后跟一串数字
    pattern = r'^https://fanqienovel\.com/page/\d+$'
    return re.match(pattern, url) is not None

if __name__ == '__main__':
    # 接受命令行输入的小说URL
    print("===================================================================")
    print("这是伟大的CYH写给YWC的小工具")
    print("感恩吧！给他带饭吧！给他拿外卖吧！请他喝奶茶吧！")
    print("===================================================================")

    download_type = input("1、要下载的小说格式为（可选：txt、epub、mobi）：")
    while True:
        if download_type not in ['txt','epub','mobi']:
            print("ERROR: 格式暂不支持或输入错误")
            download_type = input("1、要下载的小说格式为（可选：txt、epub、mobi）：")
        else:
            break

    intro_url = input("2、输入小说简介页面的URL（格式：https://fanqienovel.com/page/7301659434223143948）：")
    while True:
        if not is_valid_url(intro_url):
            print("ERROR: URL格式不符合预期格式")
            intro_url = input("2、输入小说简介页面的URL（格式：https://fanqienovel.com/page/7301659434223143948）：")
        else:
            break

    print("\n 开始下载 ~ \n")

    save_path = info.get_novel_info(url=intro_url)
    content.download(path=save_path, type=download_type)

    print('===================================================================')
    print('已经下载完毕 ~ 详情见download文件夹下')

    os.system('pause')  # 按任意键退出
