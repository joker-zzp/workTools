from lib.web.base import (
    web_open,
    web_option,
    web_close,
    web_get,
)
from lib.conf import get_ini_conf
from selenium import webdriver
import time


def main():
    PATH = 'configs/web.ini'
    conf = get_ini_conf(PATH)
    web_conf = conf.get('web_conf')
    web_conf.update({
        'user_dir': web_conf.get('user_dir') + '00'
    })
    params = web_option('chrome', **web_conf)
    browser, err = web_open('chrome', **params)
    # time.sleep(1)
    url = 'https://www.baidu.com'
    _, err = web_get(browser, url)
    print(err)
    web_close(browser)
