# import package
try:
    import os
    import requests
    import datetime
    from html.parser import HTMLParser
except Exception as e:
    raise


# 產生 png 檔案
def make_sticker(sticker_name, img_url_list):
    # 資料夾名稱：貼圖名稱_年_月_日_時_分_秒（避免重複）
    now      = datetime.datetime.now()
    date     = '{0}_{1}_{2}_{3}_{4}_{5}'.format(now.year, now.month, now.day, now.hour, now.minute, now.second)
    py_path  = os.path.dirname(os.path.realpath(__file__))
    folder   = '{0}/{1}_{2}'.format(py_path, sticker_name, date)
    count    = 0

    os.system('mkdir {0}'.format(folder))
    for img_url in img_url_list:
        count += 1
        with open('{0}/{1}_{2}.png'.format(folder, sticker_name, str(count)), 'wb') as sticker:
            try:
                img = requests.get(img_url)
            except Exception as e:
                print('No network.')
            else:
                for chunk in img:
                    sticker.write(chunk)

    print('Done.')


# 處理 html 並取得貼圖網址
def parse_web(url_result):
    # HTMLParser
    class Get_web_HTMLParser(HTMLParser):
        """
        一張貼圖的 html

        <span
            class="mdCMN09Image"
            style="
                width: 150px;
                height: 133px;
                background-image:url(https://sdl-stickershop.line.naver.jp/products/0/0/1/7028/android/stickers/12771399.png);
                background-size: 150px 133px;"
            data-sticker-id="12771399">
        </span>
        """

        in_sticker_name = False
        sticker_name    = 'no'
        img_url_list    = []

        def handle_starttag(self, tag, attrs):
            if tag == 'h3':
                for attr in attrs:
                    if attr[0] == 'class' and attr[1] == 'mdCMN08Ttl':
                        self.in_sticker_name = True
            elif tag == 'span':
                dict_attrs = dict(attrs)
                # 不一定每個 span 標籤都有 class 屬性
                try:
                    if dict_attrs['class'] == 'mdCMN09Image':
                        self.img_url_list.append(dict_attrs['style'].split(';')[2].split('(')[1].split(')')[0])
                except Exception as e:
                    pass

        def handle_endtag(self, tag):
            pass

        def handle_data(self, data):
            if self.in_sticker_name:
                self.sticker_name    = data
                self.in_sticker_name = False

    # 簡易的判斷是否為貼圖網頁
    html = url_result.text
    if '點擊貼圖即可預覽' in html and '贈送禮物' in html:
        parser = Get_web_HTMLParser()
        parser.feed(html)
        make_sticker(parser.sticker_name, parser.img_url_list)
    else:
        print('This is not a Line sticker page.')


# 取得 html
def get_web():
    try:
        print('Get some sticker here: https://store.line.me/home/zh-Hant')

        url        = input('Please input your sticker url: ')
        url_result = requests.get(url)
    except Exception as e:
        if url == '':
            print('No url input.')
        else:
            print('No network.')
    else:
        # 確認有得到網頁的資訊
        if url_result.status_code == 200:
            parse_web(url_result)
        else:
            print('Get web error.')


def main():
    get_web()


if __name__ == '__main__':
    main()
