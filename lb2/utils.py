import html
import urllib.parse

def parse_post_data(content_length, rfile):
    #читает тело POST-запроса и возвращает словарь параметров
    post_data = rfile.read(int(content_length)).decode('utf-8')
    return {k: v[0] for k, v in urllib.parse.parse_qs(post_data).items()}