
from lsminer import *
import time
import socket
import uuid
import json
import os
import logging
import queue
import threading

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

q = queue.Queue(0)

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
        self.sock.setblocking(True)
        self.sock.settimeout(None)
        self.sock.sendall(reqjson.encode("utf-8"))


    def loadCfg(self):
        self.cfg = loadCfg()
        if self.cfg == 0:
            raise ValueError('loadcfg error!')
        if 'ip' not in self.cfg or 'port' not in self.cfg:
            raise ValueError('config file error. missing ip or port!')

    def processMsg(self, msg):
        if 'method' in msg:
            if msg['method'] == 1:
                pass
            elif msg['method'] == 2:
                pass
            elif msg['method'] == 3:
                pass
            elif msg['method'] == 4:
                pass
            elif msg['method'] == 5:
                pass
            elif msg['method'] == 6:
                pass
            elif msg['method'] == 7:
                pass
            elif msg['method'] == 8:
                pass
            elif msg['method'] == 9:
                pass
            elif msg['method'] == 10:
                pass
            elif msg['method'] ==11:
                pass
            elif msg['method'] == 12:
                pass
            elif msg['method'] == 13:
                pass
            elif msg['method'] == 14:
                pass
            else:
                print('unknown server msg method! msg: ' + str(msg))
        else:
            print('unknown server msg! msg: ' + str(msg))


    def recvThread(self):
        buffer = []
        while True:
            if self.sock == None:
                print('client socket == None. sleep one second.')
                time.sleep(1)
                continue

            rd = self.sock.recv(4096).decode()
            if rd:
                buffer.append(rd)
                data = ''.join(buffer)
                try:
                    msg = json.loads(data)
                    self.processMsg(msg)
                    buffer.clear()
                except Exception as e:
                    print('recv thread exception. msg: ' + str(e))
                    print('json.loads server data exception.')
            else:
                print('server close socket. exit recv thread.')
                self.sock.close()
                break

    def processCmd(self, cmd):
        pass

    def init(self):
        self.loadCfg()
        #self.loginSrv()
        thread = threading.Thread(target=lsminerClient.recvThread, args=(self,))
        thread.start()

    def run(self):
        q.put(1)
        while True:
            try:
                cmd = q.get()
                self.processCmd(cmd)
            except Exception as e:
                print("main loop run exception. msg: " + str(e))
                print("sleep 3 seconds and retry...")
                time.sleep(3)


if __name__ == '__main__':
    client = lsminerClient()
    client.init()
    client.run()



    


