import os
import sys
import requests

from PIL import Image

from html.parser import HTMLParser


WORKING_DIR = os.path.dirname(os.path.realpath(__file__))


class StickerHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()

        self.in_sticker_name = False
        self.sticker_name = ''
        self.image_urls = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('class') == 'mdCMN08Ttl' and tag == 'h3':
            self.in_sticker_name = True
        elif attrs.get('class') == 'mdCMN09Image' and tag == 'span':
            url = attrs.get('style').split('(')[1].split(')')[0]
            self.image_urls.append(url.split(';')[0])

    def handle_data(self, data):
        if self.in_sticker_name:
            self.sticker_name = data

    def handle_endtag(self, tag):
        if tag == 'h3' and self.in_sticker_name:
            self.in_sticker_name = False


def save(name, urls):
    folder_path = os.path.join(WORKING_DIR, 'sticker-{}'.format(name))
    count = 0
    image_path_list = []
    os.mkdir(folder_path) if not os.path.exists(folder_path) else None
    for url in urls:
        count += 1
        sticker_path = os.path.join(folder_path, '{}-{}.png'.format(name, count))
        with open(sticker_path, 'wb') as sticker:
            image = requests.get(url)
            [sticker.write(chunk) for chunk in image]
        image_path_list.append(sticker_path)
        print('Downloading...... {}/{}'.format(count, len(urls)), end='\r')

    print()
    return count, folder_path, image_path_list


def resize(max_size, image_path_list):
    try:
        max_size = int(max_size)
    except Exception:
        return 'size you input is not a number, resize fail'

    for image_path in image_path_list:
        image = Image.open(image_path)
        width, height = image.size
        if width > height:
            height, width = int(max_size / width * height), max_size
        else:
            width, height = int(max_size / height * width), max_size

        image.resize((width, height), Image.BILINEAR).save(image_path)
        image.close()

    return 'finish'


def main():
    url = sys.argv[1] if len(sys.argv) >= 2 else input('Your sticker url: ')
    max_size = sys.argv[2] if len(sys.argv) >= 3 else input('Your resize size, input "no" for no resize: ')
    res = requests.get(url)
    if res.status_code != 200:
        print('Get sticker page error, status code {}.'.format(res.status_code))
        exit()

    parser = StickerHTMLParser()
    parser.feed(res.text)
    count, folder_path, image_path_list = save(parser.sticker_name, parser.image_urls)
    resize_reult = resize(max_size, image_path_list) if max_size != 'no' else 'no resize'

    print('information:')
    print('  total: {}'.format(count))
    print('  output path: {}'.format(folder_path))
    print('  resize: {}'.format(resize_reult))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nExit by user')
