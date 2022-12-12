#%%
from zipfile import ZipFile
import requests
import urllib3
import shutil

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def download_unzip(url, path, chunk_size=128):
    resposta = requests.get(url, verify=False)
    with open(path, 'wb') as fd:
        for chunk in resposta.iter_content(chunk_size=chunk_size):
            fd.write(chunk)
    
    with ZipFile(path,"r") as zip_ref:
        zip_ref.extractall(".")

def remover_arquivos(path):
    shutil.rmtree(path) 


