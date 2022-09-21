from utils.Jreq import JRequest, Response
from lib.data import dict_json, json_dict
import re

class Fmz_Api:

    def __init__(self):
        self.service = {
            'jayce': 'jayce.api.mediatrack.cn',
            'kayle': 'kayle.api.mediatrack.cn',
        }
        self.req = None
        self.server = None
        self.res = None

    def set_server(self, service):
        if self.service.get(service):
            server = self.service.get(service)
            if self.server:
                if self.server != server:
                    self.server = server
                    self.req = JRequest(server = f'https://{self.server}')
                else:
                    pass
            else:
                self.server = server
                self.req = JRequest(server = f'https://{self.server}')
        else:
            raise Exception('service not in self.service')
    
    def set_tocken(self, tocken):
        self.tocken = tocken

    def send(self, temp: dict, data: dict, new_params:dict = {}):
        # 设置服务 如果服务一致会跳过
        self.set_server(service = temp.get('service'))
        
        # 请求头处理
        self.req.set_headers()
        self.req.up_headers(head = {
            'authorization': f'Bearer {self.tocken}'
        })

        # 参数处理
        # 必要参数 检查&替换
        need_params = temp.get('need_params')
        if set(need_params) <= set(data):
            params = temp.get('default_data').copy()
            # 新参数替换 旧参数 和 旧数据
            if new_params:
                params.update(new_params)
                # 新参数 与 必填数据有交集
                if set(need_params) & set(new_params.keys()):
                    for i in set(need_params) & set(new_params.keys()):
                        data.update({i: new_params.get(i)})

            # 参数转 json 进行字符串替换
            params = dict_json(dict_data = params)
            if need_params:
                for i in need_params:
                    if f'${{{i}}}' in temp.get('api'):
                        tmp_api = temp.get('api')
                        temp.update({'api': str(temp.get('api')).replace(f'${{{i}}}', data.get(i))})
                    if f'${{{i}}}' in params:
                        params = params.replace(f'${{{i}}}', data.get(i))
            params = json_dict(data = params)
            if not params: params = None
        else:
            miss_params = set(need_params) - set(data)
            raise Exception(f'params miss: {miss_params}')

        # api 处理
        self.req.set_api(api = temp.get('api'))
        print(self.req.api)
        # 执行
        if str(temp.get('r_type')).lower() in ['post', 'put']:
            res: Response = getattr(self.req, str(temp.get('r_type')).lower())(params = params, upload_type = 'json')
        else:
            res: Response = getattr(self.req, str(temp.get('r_type')).lower())(params = params)
        if res.status_code == 200:
            self.res = res.json()
        else:
            self.req = None
        
