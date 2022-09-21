import requests

def _wechat_req(wx_url:str, doc:dict):
    """微信 请求发送

    Args:
        wx_url (str): 连接地址
        doc (dict): 数据体
    """
    res, err = True, None
    base_head = {
        'Content-Type': 'application/json'
    }
    try:
        res = requests.post(
            url=wx_url,
            headers=base_head,
            json=doc
        )
        data = res.json()
    except Exception as e:
        res, err = False, e
    else:
        if data.get('errcode'):
            res, err = False, data
    finally:
        return res, err

def send_msg(key:str, text:str = None) -> tuple:
    """发送消息

    Args:
        key (str): 密钥 key
        text (str, optional): text 文本. Defaults to None.

    Returns:
        tuple: 发送结果
    """
    res, err = True, None
    # 设置发送消息的 url
    url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}'
    # 设置数据体
    doc = {
        'msgtype': 'text',
        'text': {
            'content': text if text else 'hello world!'
        }
    }
    res, err = _wechat_req(url, doc)
    return res, err

def send_file(key:str, file:str) -> tuple:
    """发送文件

    Args:
        key (str): 密钥 key
        file (str): 文件路径

    Returns:
        tuple: 发送结果
    """
    res, err = True, None
    try:
        # 文件发送地址
        tmp_file_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={key}&type=file'
        # 构造数据体
        data = {'file': open(file, 'rb')}
        # 发送文件
        req = requests.post(url=tmp_file_url, files=data)
    except Exception as e:
        res, err = False, e
        return
    else:
        json_res = req.json()
        # 获取临时文件id
        m_id = json_res.get('media_id')
        data = {
            'msgtype': 'file',
            'file': {'media_id': m_id}
        }
        url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}'
        res, err = _wechat_req(url, data)
    finally:
        return res, err
