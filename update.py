#!/usr/bin/python3
from lsminer import *
import os
import sys
import time
from urllib import request
from urllib import parse
import subprocess
import tarfile
import hashlib


headers = {
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Cache-Control': 'no-cache',
    'Content-Type':'application/x-www-form-urlencoded',
    'User-Agent':'lsminer client for linux'
    }
 
#url = "http://lsminer.yunjisuan001.com:23335/appupdate_linux"

def get_file_md5(file_path):
    """
    获取文件md5值
    :param file_path: 文件路径名
    :return: 文件md5值
    """
    with open(file_path, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        _hash = md5obj.hexdigest()
    return str(_hash).lower()


def checkClientUpdate(ver, url):
    ''' return true = client has been updated or false = client has not been updated.'''
    try:
        body = {}
        body['version'] = ver
        data = parse.urlencode(body).encode('utf-8')
        req = request.Request(url, headers=headers, data=data)
        with request.urlopen(req) as f:
            resdict = json.loads(f.read().decode('utf-8'))

        if resdict['result']:
            filepath = './' + resdict['appname']
            while True:
                if downloadFile(resdict['appurl'], filepath):
                    if get_file_md5(filepath) == resdict['appmd5']:
                        with tarfile.open(filepath) as tar:
                            tar.extractall('./miners')
                            #os.remove(path)
                            
                        cfg = loadCfg()
                        cfg['appver'] = resdict['appver']
                        if saveCfg(cfg):
                            print("config file appver update ok.")
                    else:
                        print("lsminer client package md5 hash wrong. sleep 3 seconds and try later.")
                else:
                    print("download lsminer client package file failed. sleep 3 seconds and try later.")
                time.sleep(3) 
        else:
            print(resdict['error'])

    except Exception as e:
        print("function reportThread exception. msg: " + str(e))

if __name__ == '__main__':
    try:
        cfg = loadCfg()
        if cfg == 0:
            raise ValueError('loadcfg error!')
        if 'appver' not in cfg or 'updateapi' not in cfg:
            raise ValueError('config file error. missing updateapi or appver!')
        
        if checkClientUpdate(cfg['appver'], cfg['updateapi']):
            print('client has been updated. lsminer client will restart later.')
            sys.exit(1)
        
        while True:
            process = subprocess.run('python3 ./client.py')
            if process.returncode == 123:
                if checkClientUpdate(cfg['appver'], cfg['updateapi']):
                    print('client has been updated. lsminer client will restart later.')
                    sys.exit(1)
                else:
                    print('client recv update msg, but version in server is not updated!')

    except Exception as e:
        print('update.py function __main__ exception. msg: ' + str(e))

    