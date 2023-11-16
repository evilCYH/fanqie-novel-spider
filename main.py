import chapter_info as info
import chapter_content as content

if __name__ == '__main__':
    headers = [
        {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
        },
        {
            "User-Agent": 'Mozilla/5.0 (Linux; Android 11; MI 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36'
        }
    ]
    intro_url = 'https://fanqienovel.com/page/7130527328643320832?enter_from=search'
    info.get_novel_info(url = intro_url, headers = headers[0])
    content.create_epub(headers = headers[1], path = info.save_path)
    print(f'========================================================================')
    print(f'全部章节 已经下载完毕~')
    # content.get_chapter_content(headers = headers[1], path = info.save_path)