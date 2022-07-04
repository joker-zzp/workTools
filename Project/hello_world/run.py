# 在此 导入 main 方法替换此main方法 使用 from src.main import main

def main():
    print('hello world')

def __main__():main()

if __name__ == "__main__":
    __main__()
