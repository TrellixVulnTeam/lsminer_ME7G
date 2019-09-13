#!/usr/bin/python3
from tools import *
import os
import sys
import time
from urllib import request
from urllib import parse
import subprocess
import tarfile
import hashlib

import logging

logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt = '%Y-%m-%d  %H:%M:%S %a')

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
            filepath = './update.tar.gz'
            while True:
                if downloadFile(resdict['appurl'], filepath):
                    if get_file_md5(filepath) == resdict['appmd5']:
                        print('file download ok.')
                        #with tarfile.open(filepath) as tar:
                            #tar.extractall('./')
                            #os.remove(path)
                    else:
                        logging.warning("lsminer client package md5 hash wrong. sleep 3 seconds and try later.")
                else:
                    logging.warning("lsminer client download lsminer client package file failed. sleep 3 seconds and try later.")
                time.sleep(3) 
        else:
            logging.error(resdict['error'])

    except Exception as e:
        logging.error("function reportThread exception. msg: " + str(e))
        logging.exception(e)

def stopService():
    subprocess.run('systemctl stop redline', shell=True)
    subprocess.run('systemctl stop teleconsole', shell=True)
    subprocess.run('systemctl stop miner', shell=True)

def startService():
    subprocess.run('systemctl start redline', shell=True)
    subprocess.run('systemctl start teleconsole', shell=True)
    subprocess.run('systemctl start miner', shell=True)

def checkLocalUpdate():
    try:
        filepath = './update.tar.gz'
        if os.path.exists(filepath):
            stopService()
            with tarfile.open(filepath) as tar:
                tar.extractall('./')
            startService()

    except Exception as e:
        logging.error("function checkLocalUpdate exception. msg: " + str(e))
        logging.exception(e)

if __name__ == '__main__':
    try:
        cfg = loadCfg()
        updateurl = cfg['updateapi']
        appver = getClientVersion()

        if checkLocalUpdate(appver):
            sys.exit(1)

        if checkClientUpdate(appver, updateurl):
            logging.info('client has been updated. lsminer client will restart later.')
            subprocess.run('systemctl restart miner', shell=True)
            sys.exit(1)
        
        while True:
            process = subprocess.run('python3 ./client.py', shell=True)
            if process.returncode == 123:
                if checkClientUpdate(appver, updateurl):
                    logging.info('client has been updated. lsminer client will restart later.')
                    subprocess.run('systemctl restart miner', shell=True)
                    sys.exit(1)
            else:
                logging.warning('client exit! sleep 3 seconds and try start again.')
                time.sleep(3)

    except Exception as e:
        logging.error('update.py function __main__ exception. msg: ' + str(e))
        logging.exception(e)
    