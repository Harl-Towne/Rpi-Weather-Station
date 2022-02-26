# random file full of useful functions
import os
import pandas as pd


def recursive_mkdir(path: str):
    if os.path.exists(path):
        return
    base, folder = os.path.split(path)
    recursive_mkdir(base)
    os.mkdir(path)


def safe_save_dataframe(data: pd.DataFrame, file_name: str, path: str):
    files = os.listdir(path)
    file = os.path.join(path, file_name)
    if file_name in files and os.path.isfile(file):
        # if the file already exists save a backup first
        file_bak = os.path.join(path, file_name + ".bak")
        data.to_csv(file_bak, index=False)
        os.remove(file)
        os.rename(file_bak, file)
    else:
        # if not just save the file
        data.to_csv(file, index=False)
