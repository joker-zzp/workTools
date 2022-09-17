from smb.SMBConnection import SMBConnection
import os

def connet(server:dict) -> SMBConnection:
    """smb 链接

    Args:
        server (dict): smb 配置 ip, prot, username, password

    Returns:
        SMBConnection: _description_
    """
    ip = server.pop('ip')
    prot = server.pop('prot') if server.get('prot') else 139
    if not server.get('my_name'): server['my_name'] = ''
    if not server.get('remote_name'): server['remote_name'] = ''
    conn = SMBConnection(**server)
    conn.connect(ip, prot, timeout=20)
    return conn

def upload(obj:SMBConnection, service_name:str, path:str, file_path:str):
    """上传文件 scp

    Args:
        obj (SMBConnection): 链接对象
        service_name (str): 服务名称 磁盘名 根节点
        path (str): 目标路径 ps: 此路径文件路径 不会创建文件夹 如果文件夹不存在则异常
        file_path (str): 本地文件路径
    """
    with open(file_path, 'rb') as file_obj:
        obj.storeFile(service_name, path, file_obj)
        # print(res)

def mkdir(obj:SMBConnection, service_name, path:str):
    res = obj.createDirectory(service_name, path)

def close(obj:SMBConnection):
    """关闭链接

    Args:
        obj (SMBConnection): 链接对象
    """
    obj.close()
