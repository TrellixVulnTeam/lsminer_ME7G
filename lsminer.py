from urllib import request
import time
import socket
import uuid
import json
import os
import hashlib
import gpumon

def getMac():
    '''获取系统网卡MAC地址'''
    macnum = hex(uuid.getnode())[2:]
    mac = "-".join(macnum[i: i+2] for i in range(0, len(macnum), 2))
    return mac

def getName():
    '''获取电脑名称'''
    return socket.gethostname()

def getIp():
    '''获取系统内网IP地址'''
    return socket.gethostbyname(getName())

def getAccessKey():
    try:
        with open("/home/lsminer.conf", "r", encoding="utf-8") as fs:
            key = fs.readline()
            return key
    except Exception as e:
        print("function getAccessKey exception. msg: " + str(e))
    return 0

def loadCfg():
    '''加载当前目录下的配置文件config.json'''
    try:
        with open("./config.json", "r", encoding="utf-8") as fs:
            cfg = json.load(fs)
        if not cfg['accesskey']:
            cfg['accesskey'] = getAccessKey()
            saveCfg(cfg)
        return cfg
    except Exception as e:
        print("function loadCfg exception. msg: " + str(e))
    return 0
    

def saveCfg(cfgdict):
    '''保存当前目录下的配置文件config.json'''
    try:
        with open("./config.json", "w", encoding="utf-8") as fs:
            json.dump(cfgdict, fs)
            return 1
    except Exception as e:
        print("function saveCfg exception. msg: " + str(e))
    return 0
    
def md5(data):
    '''MD5哈希函数'''
    return str(hashlib.md5(data.encode('utf-8')).hexdigest())

def getWkid():
    '''获取Wkid(网卡MAC字符串MD5哈希值)'''
    return md5(getMac())

def getReboot(url):
    '''检测是否需要重启系统'''
    try:
        req = request.Request(url)
        with request.urlopen(req) as f:
            return int(f.read().decode('utf-8'))
    except Exception as e:
        print("function getReboot exception. msg: " + str(e))
    return 0

def getNvidiaCount():
    '''获取NVIDIA显卡的数量'''
    count = 0
    pci = os.popen('lspci').read().splitlines(False)
    for l in pci:
        if 'VGA' in l or '3D controller' in l:
            if 'NVIDIA' in l and 'nForce' not in l:
                count += 1
    return count

def getAMDCount():
    '''获取AMD显卡的数量'''
    count = 0
    pci = os.popen('lspci').read().splitlines(False)
    for l in pci:
        if 'VGA' in l or '3D controller' in l:
            if 'Advanced Micro Devices' in l and 'RS880' not in l:
                count += 1
    return count

def getVedioCard():
    '''获取显卡列表'''
    cardstr = ""
    pci = os.popen('lspci').read().splitlines(False)
    for l in pci:
        if 'VGA' in l or '3D controller' in l:
            name = l.split(': ')[1].strip()
            if cardstr:
                cardstr = cardstr + "|" + name
            else:
                cardstr = name
    return cardstr
    
def downloadFile(url, path):
    '''从url下载文件保存到path路径，path包含文件名'''
    try:
        req = request.Request(url)
        with request.urlopen(req) as f:
            with open(path, "wb") as p:
                p.write(f.read())
                p.flush()
                return 1
    except Exception as e:
        print("function downloadFile exception. msg: " + str(e))
    return 0

