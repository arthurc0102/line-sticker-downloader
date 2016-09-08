# import package
try:
    import os
    import requests
    from html.parser import HTMLParser
except Exception as e:
    raise


def parse_web(url_result):
    # HTMLParser
    class Get_web_HTMLParser(HTMLParser):
        in_sticker_name = False
        sticker_name    = 'no'

        def handle_starttag(self, tag, attrs):
            if tag == 'h3':
                for attr in attrs:
                    if attr[0] == 'class' and attr[1] == 'mdCMN08Ttl':
                        self.in_sticker_name = True

        def handle_endtag(self, tag):
            pass

        def handle_data(self, data):
            if self.in_sticker_name:
                self.sticker_name    = data
                self.in_sticker_name = False

    # 簡易的判斷是否為貼圖網頁
    html = url_result.text
    if html.find('點擊貼圖即可預覽') != -1 and html.find('贈送禮物') != -1:
        parser = Get_web_HTMLParser()
        parser.feed(html)
        print(parser.sticker_name)
    else:
        print('This is not a Line sticker page.')


def get_web():
    # url        = input('Please input your sticker url: ')
    url        = 'https://store.line.me/stickershop/product/7028/zh-Hant'
    url_result = requests.get(url)

    # 確認有得到網頁的資訊
    if url_result.status_code == 200:
        parse_web(url_result)
    else:
        print('Get web error.')


def main():
    get_web()


if __name__ == '__main__':
    main()
