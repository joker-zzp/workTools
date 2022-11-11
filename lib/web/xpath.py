from .base import (
    web_find_xpath,
    web_not_find_xapth
)
from .base import Keys


# 点击
@web_find_xpath(timeout = 5)
def web_click(browser, tag_xpath):
    try:
        browser.find_element_by_xpath(tag_xpath).click()
    except Exception as e:
        err = e
    else:
        err = None
    finally:
        return browser, err

# 输入
@web_find_xpath(timeout = 5)
def web_input(browser, tag_xpath, value):
    try:
        browser.find_element_by_xpath(tag_xpath).send_keys(value)
    except Exception as e:
        err = e
    else:
        err = None
    finally:
        return browser, err

# 清除
@web_find_xpath(timeout = 5)
def web_input_clear(browser, tag_xpath):
    try:
        element = browser.find_element_by_xpath(tag_xpath)
        val = element.get_attribute('value')
        for i in val:
            element.send_keys(Keys.BACKSPACE)
    except Exception as e:
        err = e
    else:
        err = None
    finally:
        return browser, err

# 悬停

# 检查 值

# 检查 不存在

# 检查 可点击

# 检查 不可点击
