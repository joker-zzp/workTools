import zipfile

def decode_file(file_path:str, to_dir:str):
    with zipfile.ZipFile(file=file_path) as zf:
        zf.extractall(path=to_dir)
        zf.close()
