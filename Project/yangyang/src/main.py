import random
import string
from lib.data import json_dict, dict_json


def print_maps(data):
    # _init_map = [[0 for _ in range(13)] for _ in range(13)]
    # data = {}
    for i in data:
        print(' '.join([str(s) if s else ' ' for s in i]))

def map_sum_data(data:list) -> list:
    res = []
    for y in range(len(data)):
        for x in range(len(data)):
            if data[y][x]:
                res.append(f'{y}_{x}')
                # print(y, x)
    return res

def random_three(t:dict, data:list):
    # 获取长度 40 概率 直接填3个
    data_len = len(data)
    len_3 = None
    if data_len < 4:
        # 50 概率 3 连
        if random.choice([1, 0]):
            # 填 3 个
            len_3 = True
    else:
        # 必填 3 个
        len_3 = True
    # 随机拿一个
    r_key = random.choice(list(t.keys()))
    if len_3:
        # 随机到已有数据 只添加一个
        if r_key in data:
            data.insert(data.index(r_key), r_key)
            t[r_key] -= 1
        else:
            for _ in list(r_key * 3):
                data.insert(0, r_key)
            t[r_key] -= 3
    else:
        data.append(r_key)
        t[r_key] -= 1
    return r_key


def map_edcode(map_data:list, type_num):
    res = []
    # 总层数
    c_count = len(map_data)
    # 循环每层定义坐标
    tmp_data = {}
    for c in range(c_count):
        tmp_data.update({c: list(map(lambda x: f'{c}_' + x, map_sum_data(map_data[c])))})
    # 统计临时数据
    tmp_data_count = sum([len(i) for i in tmp_data.values()]) 
    # 生成随机字符
    _type = string.ascii_uppercase[0:type_num]
    
    data = {i: tmp_data_count // 3 for i in list(_type)}
    structre_c = 0
    senven_data = []
    # 循环 数据源
    while data:
        # print('------')
        rk = random_three(data, senven_data)
        print(rk, senven_data)
        # 3 消
        if senven_data.count(rk) == 3:
            # 随机找 3 个位置进行填充
            tmp = []
            for _ in range(3):
                # 随机找第一层 没有找下一层
                if not tmp_data.get(structre_c):
                    structre_c += 1
                y_x = random.choice(tmp_data.get(structre_c))
                _c, _y, _x = [int(i) for i in str(y_x).split('_')]
                map_data[_c][_y][_x] = rk
                tmp.append(y_x)
                tmp_data.get(structre_c).remove(y_x)
                senven_data.remove(rk)
            res.append({rk: tmp.copy()})
        if not data.get(rk):
            data.pop(rk)
    print(res)
    print(map_data)

def debug(data):
    
    pass

def main():
    data_path = 'data/map.json'
    conf_data = json_dict(file_path=data_path)
    print()
    map_data = conf_data.get('one')
    # print_maps(map_data)
    type_num = 3
    
    map_edcode(map_data, type_num)
    
    # debug
    # debug()

    # print(123)
    pass