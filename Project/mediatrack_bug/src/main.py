from lib.data import dict_json, json_dict, dict_find_key
from lib.conf import get_ini_conf
from src.api import Fmz_Api
from lib.data import urldecode

CONF_PATH = 'configs/main.ini'

def find_key(data:dict, temp:dict) -> dict:
    res = {}
    for k, v in temp.items():
        tmp = dict_find_key(data, json_path = v)
        if tmp:
            if len(tmp) == 1:
                res.update({k: tmp[0]})
            else:
                res.update({k: tmp.copy()})
        del tmp
    return res

def main():
    conf = get_ini_conf(path = CONF_PATH)
    api_conf: dict = conf.get('api')
    api_menu_data = json_dict(file_path = api_conf.get('menu_data'))
    run_step = json_dict(file_path = api_conf.get('run_step'))
    menu = [f'{i}: {v.get("doc")}' for i, v in api_menu_data.items()]
    print(menu)

    obj_api = Fmz_Api()

    # 需要参数
    need_params = set([k for i in run_step.keys() for k in api_menu_data.get(i).get('need_params')])

    # 参数支持
    params_data = {}

    tocken = ''
    # 读取临时文件中 tocken
    if tocken_path := api_conf.get('run_tocken'):
        with open(tocken_path, 'r') as f:
            tocken = f.read()
    # 设置 tocken
    obj_api.set_tocken(tocken)

    # debug_count = 0
    # 运行
    for k, v in run_step.items():
        # api 发送
        obj_api.send(temp = api_menu_data.get(k), data = params_data, new_params = v.get('new_params'))
        # 参数更新
        params_data.update(find_key(obj_api.res, temp = v.get('res_done') if v.get('res_done') else {}))
        # debug
        # debug_count += 1
        # if debug_count == 3:
        #     print(dict_json(dict_data = obj_api.res))
        #     print(params_data)
    print()
    print(params_data.get('short_url'))
