
from lsminer import *
import time
import socket
import uuid
import json
import os
import logging

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class lsminerClient(object):
    def __init__(self):
        self.state = None
        self.cfg = None
        self.sock = None

    def __del__(self):
        pass
    
    def getResp(self):
        pass

    def loginSrv(self):
        n = getNvidiaCount()
        a = getAMDCount()
        reqData = {}
        reqData['method'] = 1
        reqData['accesskey'] = self.cfg['accesskey']
        reqData['wkname'] = self.cfg['wkname']
        reqData['wkid'] = getWkid()
        reqData['devicename'] = getVedioCard()
        reqData['devicecnt'] = a + n
        reqData['appver'] = self.cfg['appver']
        reqData['platform'] = 1 if n > a else 2
        reqData['driverver'] = self.cfg['driverver']

        reqjson = json.dumps(reqData)
        logging.info(reqjson)
        self.sock = socket.create_connection((self.cfg['ip'], self.cfg['port']), 3)
        self.sock.sendall(reqjson)


    def loadCfg(self):
        self.cfg = loadCfg()
        if self.cfg == 0:
            raise ValueError('loadcfg error!')
        if 'ip' not in self.cfg or 'port' not in self.cfg:
            raise ValueError('config file error. missing ip or port!')

while True:
    try:
        client = lsminerClient()
        client.loadCfg()

    except Exception as e:
        print("main loop run exception. msg: " + str(e))
        print("sleep 3 seconds and retry.")
        time.sleep(3)
    
    


