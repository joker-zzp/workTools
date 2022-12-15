from lib.conf import get_ini_conf
from lib.data import urldecode, urlencode
from lib.data import json_dict, dict_json
from lib.data import re_get_str
from lib.web.html import html_xpath, element_xpath
from utils.Jreq import JRequest

def get_index(server: str, url: str) -> str:
    r = JRequest(server = server)
    r.set_headers({
        'Accept-Language': 'zh-CN,zh;q=0.9',
    })
    r.set_api(api = url)
    req = r.get()
    if req.status_code == 200:
        req.encoding = 'utf-8'
        with open('tmp/index.html', 'w') as f:
            f.write(req.text)
        return req.text


def index_format(data: dict) -> dict:
    index_url = data.get('url')
    server = data.get('server')
    res = get_index(server, url = index_url)
    port = re_get_str(_r=data.get('url_re'), data=res)
    server = f'{server}:{port}'
    res = get_index(server, url = index_url)
    # tab
    video_tab_element = html_xpath(res, data.get('video_tab_xpath'))
    video_tab_data = {}
    for i in video_tab_element:
        video_tab_data.update({i.text: {'href': i.attrib.get('href')}})
    for _, i in video_tab_data.items():
        tmp = get_index(server, i.get('href'))
        tmp_data = []
        video_data = html_xpath(tmp, data.get('video_data_xpath'))
        for tag in video_data:
            tmp_tag = element_xpath(tag, './a')
            _title = tmp_tag.attrib.get('title')
            _herf = tmp_tag.attrib.get('href')
            _img_url = tmp_tag.attrib.get('data-original')
            _update = element_xpath(tag, './a/span/font').text if hasattr(element_xpath(tag, './a/span/font'), 'text') else None 
            tmp_data.append({
                'title': _title,
                'img_url': _img_url,
                'href': f'{server}{_herf}',
                'update': _update,
            })
        i.update({'data': tmp_data})
    return video_tab_data

def main():
    CONF_PATH = 'configs/server.ini'
    conf = get_ini_conf(path = CONF_PATH)
    data_conf = conf.get('data')
    data = json_dict(file_path = data_conf.get('index'))
    index_data = index_format(data)
    dict_json(dict_data = index_data, json_file = 'tmp/1.json')
