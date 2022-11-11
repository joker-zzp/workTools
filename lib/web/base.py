from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import functools


# open browser
def web_open(browser_type: str, *args, **kwargs):
    err = None
    try:
        web_obj = {
            'chrome': webdriver.Chrome,
            'firefox': webdriver.Firefox,
            'safari': webdriver.Safari,
        }
        obj = web_obj.get(browser_type.lower())
        if obj:
            browser = obj(*args, **kwargs)
        else:
            raise Exception(f'browser_type "{browser_type}" not in {web_obj.keys()}')
    except Exception as e:
        err = e
    else:
        err = None
    finally:
        return browser, err

# browser setting
def web_option(browser_type: str, **kwargs) -> dict:
    try:
        params = {}
        # 浏览器设置对象
        web_obj = {
            'chrome': webdriver.ChromeOptions,
            'firefox': webdriver.FirefoxOptions,
        }
        options = web_obj.get(browser_type.lower())()
    
        # 去 '自动执行' 提示
        # options.add_experimental_option('excludeSwitches', ['enable-automation'])

        # 设置驱动路径
        if kwargs.get('exec_path'):
            params.update({'executable_path': kwargs.get('exec_path')})

        # 设置用户路径
        if kwargs.get('user_dir'):
            user_path = kwargs.get('user_dir')
            options.add_argument(f'user-data-dir={user_path}')

        # 静默
        if kwargs.get('static'):
            options.add_argument('headless')

        # 日志
        caps = None
        if kwargs.get('log'):
            caps = {
                'browserName': 'chrome',
                'goog:loggingPrefs': {
                    'browser': 'ALL',
                    'driver': 'ALL',
                    'performance': 'ALL'
                },
                'goog:chromeOptions': {
                    'perfLoggingPrefs': {
                        'enableNetwork': True,
                        'enablePage': False
                    },
                    'w3c': False,
                }
            }
            options.add_experimental_option('perfLoggingPrefs', {
                'enableNetwork': True,
                'enablePage': False,
            })
            params.update({'desired_capabilities': caps})

    except Exception as e:
        err = e
    else:
        err = None
        params.update({
            'options': options
        })
    finally:
        return params

# close browser
def web_close(browser) -> tuple:
    """关闭浏览器

    Args:
        browser (object): 浏览器对象

    Returns:
        tuple: 浏览器对象, 异常
    """
    err = None
    try:
        browser.quit()
    except Exception as e:
        err = e
    finally:
        return browser, err

# url get
def web_get(browser, url):
    try:
        browser.get(url)
    except Exception as e:
        err = e
    else:
        err = None
    finally:
        return browser, err

# web refresh
def web_refresh(browser):
    browser.refresh()

# web run js
def web_js(browser, js_text):
    try:
        browser.execute_script(js_text)
    except Exception as e:
        err = e
    else:
        err = None
    finally:
        return browser, err

# 显性等待 -> xpath
def web_find_xpath(timeout = 10):
    """xpath find
    selenium WebDriverWait until

    Args:
        timeout (int, optional): timeout. Defaults to 10.
    """
    def decorator(func):
        @functools.wraps(func)
        def f(browser, tag_xpath, *args, **kwargs):
            err = None
            try:
                WebDriverWait(browser, timeout).until(
                    EC.presence_of_element_located((By.XPATH, tag_xpath))
                )
            except Exception:
                err = f'run: {func.__name__} timeout in find "{tag_xpath}".'
            else:
                browser, err = func(browser, tag_xpath, *args, **kwargs)
            finally:
                return browser, err
        return f
    return decorator

# 显性等待 -> No xpath
def web_not_find_xapth(timeout = 10):
    """xpath not exists
    selenium WebDriverWait - until_not

    Args:
        timeout (int, optional): timeout. Defaults to 10.
    """
    def decorator(func):
        @functools.wraps(func)
        def f(browser, tag_xpath, *args, **kwargs):
            try:
                WebDriverWait(driver, timeout).until_not(
                    EC.presence_of_element_located((By.XPATH, tag_xpath))
                )
            except Exception:
                err = f'run: {func.__name__} timeout exists "{tag_xpath}".'
            else:
                browser, err = func(browser, tag_xpath, *args, **kwargs)
            finally:
                return browser, err
        return f
    return decorator

# 显性等待 -> id
def web_find_id(timeout = 10):
    """id find
    selenium WebDriverWait k

    Args:
        timeout (int, optional): timeout. Defaults to 10.
    """
    def decorator(func):
        @functools.wraps(func)
        def f(browser, tag_id, *args, **kwargs):
            try:
                WebDriverWait(browser, timeout).until(
                    EC.presence_of_element_located((By.ID, tag_id))
                )
            except Exception:
                err = f'run: {func.__name__} timeout in find "{tag_id}".'
            else:
                browser, err = func(browser, tag_id, *args, **kwargs)
            finally:
                return browser, err
        return f
    return decorator
