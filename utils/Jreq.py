import requests
from requests import Response
import json

class JRequest(object):

    def __init__(self, server:dict|str) -> None:
        """init

        Args:
            server (dict | str): dict(conf_data) | str(url)

        Raises:
            PermissionError: 配置缺少参数
            TypeError: server type 不支持
        """
        self.server = None
        self.headers = None
        if isinstance(server, (dict, str)):
            if isinstance(server, str):
                self.server = server
            else:
                if server.get('server'):
                    if server.get('agreement'):
                        self.server = f"{server.get('agreement')}://{server.get('server')}{':'+server.get('port') if server.get('port') else ''}"
                    else:
                        self.server = f"http://{server.get('server')}{':'+server.get('port') if server.get('port') else ''}"
                else:
                    raise PermissionError(f'Error: The "server" key was not found in the object.')
        else:
            raise TypeError(f'Error: This object is not recognized。\n{server}\n')
        
    def set_headers(self, head = None):
        base_head = {
            'Content-Type': "application/json"
        }
        self.headers = head if head else base_head

    def up_headers(self, head):
        self.headers.update(head)

    def set_api(self, api):
        api = api if str(api)[0] == '/' else f'/{api}'
        self.api = self.server + api

    def get(self, params = None):
        if params:
            try:
                res = requests.get(
                    url=self.api,
                    headers=self.headers,
                    params=params
                )
            except Exception as e:
                raise e
        else:
            try:
                res = requests.get(
                    url=self.api,
                    headers=self.headers
                )
            except Exception as e:
                raise e
        return res

    def post(self, params = None, upload_type = 'from'):
        if params:
            if upload_type == 'from':
                self.up_headers({
                    'Content-Type': 'application/x-www-form-urlencoded'
                })
                try:
                    res = requests.post(
                        url=self.api,
                        headers=self.headers,
                        data=params
                    )
                except Exception as e:
                    raise e
            if upload_type == 'json':
                try:
                    res = requests.post(
                        url=self.api,
                        headers=self.headers,
                        json=params
                    )
                except Exception as e:
                    raise e
        else:
            try:
                res = requests.post(
                    url=self.api,
                    headers=self.headers
                )
            except Exception as e:
                raise e
        return res

    def put(self, params = None, upload_type = 'from'):
        if params:
            if upload_type == 'from':
                self.up_headers({
                    'Content-Type': 'application/x-www-form-urlencoded'
                })
                try:
                    res = requests.put(
                        url=self.api,
                        headers=self.headers,
                        data=params
                    )
                except Exception as e:
                    raise e
            if upload_type == 'json':
                try:
                    res = requests.put(
                        url=self.api,
                        headers=self.headers,
                        json=params
                    )
                except Exception as e:
                    raise e
        else:
            try:
                res = requests.put(
                    url=self.api,
                    headers=self.headers
                )
            except Exception as e:
                raise e
        return res

    def delete(self, params = None):
        try:
            res = requests.delete(
                url=self.api,
                headers=self.headers,
                params = params
            )
        except Exception as e:
            raise e
        return res

    def test_api(self, obj):
        res = None
        if api_path := obj.get('api_path'):
            self.set_api(api_path)
        else:
            raise Exception('Error: Missing parameter.')
        self.set_headers(obj.get('api_head') if obj.get('api_head') else None)
        if api_type := obj.get('type'):
            if api_type.lower() == 'get':
                res = self.get()
            if api_type.lower() == 'post':
                res = self.post()
        else:
            return 0
        return res
