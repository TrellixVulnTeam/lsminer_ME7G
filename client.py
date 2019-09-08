#!/usr/bin/python3
from lsminer import *
import time
import socket
import uuid
import json
import os
import logging
import queue
import threading
import sys
import subprocess
import shlex
from datetime import timedelta
from datetime import datetime
import tarfile
import signal

from gpumon import *
from minerinfo import *

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

'''
subprocess = subprocess.Popen('ping www.baidu.com -t', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
for line in iter(subprocess.stdout.readline, ''):
    print(line.decode('gbk'))
'''

#commond queue
q = queue.Queue(0)

class lsminerClient(object):
    def __init__(self):
        self.state = None
        self.cfg = None
        self.sock = None
        self.minerargs = None
        self.minerpath = None
        self.subprocess = None
        self.mthread = None
        self.rthread = None
        self.startime = datetime.now()
        self.gpuType = self.checkGpuType()    #nvidia==1, amd==2
        self.minertime = datetime.now()

    def __del__(self):
        pass

    def getClientUptimeMinutes(self):
        delta = datetime.now() - self.startime
        return delta.seconds // 60

    def getMinerUptimeMinutes(self):
        delta = datetime.now() - self.minertime
        return delta.seconds // 60

    def getGpuInfo(self):
        if self.gpuType == 1:
            return nvmlGetGpuInfo()
        else:
            return fsGetGpuInfo()

    def checkGpuType(self):
        n = nvmlGetGpuCount()
        a = fsGetGpuCount()
        return  1 if n > a else 2
        
    def connectSrv(self):
        try:
            self.sock = socket.create_connection((self.cfg['ip'], self.cfg['port']), 3)
            self.sock.setblocking(True)
            self.sock.settimeout(None)
        except Exception as e:
            logging.error('connectSrv exception. msg: ' + str(e))
            time.sleep(3)
            q.put(1)
    
    def sendLoginReq(self):
        try:
            if self.gpuType == 1:
                cnt = nvmlGetGpuCount()
                name = nvmlGetGpuName()
            else:
                cnt = fsGetGpuCount()
                name = fsGetGpuName()
            
            reqData = {}
            reqData['method'] = 1
            reqData['accesskey'] = self.cfg['accesskey']
            reqData['wkname'] = self.cfg['wkname']
            reqData['wkid'] = getWkid()
            reqData['devicename'] = name
            reqData['devicecnt'] = cnt
            reqData['appver'] = self.cfg['appver']
            reqData['platform'] = self.gpuType
            reqData['driverver'] = self.cfg['driverver']
            reqData['os'] = self.cfg['os']
            reqjson = json.dumps(reqData)
            reqjson += '\r\n'
            self.sock.sendall(reqjson.encode("utf-8"))
        except Exception as e:
            logging.error('sendLoginReq exception. msg: ' + str(e))
            return None     

    def sendGetMinerArgsReq(self):
        try:
            reqData = {}
            reqData['method'] = 2
            reqData['os'] = self.cfg['os']
            reqjson = json.dumps(reqData)
            reqjson += '\r\n'
            self.sock.sendall(reqjson.encode("utf-8"))
        except Exception as e:
            logging.error('sendGetMinerArgsReq exception. msg: ' + str(e))
            return None

    def sendLogoutReq(self):
        try:
            reqData = {}
            reqData['method'] = 6
            reqData['os'] = self.cfg['os']
            reqjson = json.dumps(reqData)
            reqjson += '\r\n'
            self.sock.sendall(reqjson.encode("utf-8"))
        except Exception as e:
            logging.error('sendLogoutReq exception. msg: ' + str(e))
            return None

    def loadCfg(self):
        try:
            self.cfg = loadCfg()
            if self.cfg == 0:
                raise ValueError('loadcfg error!')
            if 'ip' not in self.cfg or 'port' not in self.cfg:
                raise ValueError('config file error. missing ip or port!')
        except Exception as e:
            logging.error('sendGetMinerArgsReq exception. msg: ' + str(e))
            return None

    def onWelcome(self, msg):
        logging.info('connect server ok. recv server msg: ' + msg['message'])
        q.put(2)

    def onLoginResp(self, msg):
        if 'result' in msg and msg['result']:
            logging.info('login ok.')
            q.put(3)
        else:
            logging.info('login error. msg: ' + msg['error'])
            q.put(6)
            time.sleep(1)
            q.put(1)
    
    def getReportData(self, mcfg):
        try:
            reqData = {}
            reqData['method'] = 3
            reqData['uptime'] = self.getMinerUptimeMinutes()
            reqData['minerstatus'] = 1
            gpuinfo = self.getGpuInfo()
            if gpuinfo:
                minerinfo = getMinerStatus(mcfg)
                if not minerinfo:
                    reqData['hashrate'] = 0
                    for i in range(len(gpuinfo)):
                        gpustatus = str(i) + '|'+ gpuinfo[i]['name'] + '|' + str(gpuinfo[i]['tempC']) + '|0|' + str(gpuinfo[i]['fanpcnt']) + '|' + str(gpuinfo[i]['power_usage'])
                        if i+1 == len(gpuinfo):
                            gpustatus += '$'
                        else:
                            gpustatus += '|'
                else:
                    reqData['hashrate'] = minerinfo['totalhashrate']
                    mc = len(minerinfo['hashrate'])
                    for i in range(len(gpuinfo)):
                        if i < mc:
                            gpustatus = str(i) + '|'+ gpuinfo[i]['name'] + '|' + str(gpuinfo[i]['tempC']) + '|' + str(minerinfo['hashrate'][i]) + '|' + str(gpuinfo[i]['fanpcnt']) + '|' + str(gpuinfo[i]['power_usage'])
                        else:
                            gpustatus = str(i) + '|'+ gpuinfo[i]['name'] + '|' + str(gpuinfo[i]['tempC']) + '|0|' + str(gpuinfo[i]['fanpcnt']) + '|' + str(gpuinfo[i]['power_usage'])
                        
                        if i+1 == len(gpuinfo):
                            gpustatus += '$'
                        else:
                            gpustatus += '|'
                gpustatus += str(self.getClientUptimeMinutes())
                reqData['gpustatus'] = gpustatus
                reqData = json.dumps(reqData) + '\r\n'
                return reqData
            return None
        except Exception as e:
            logging.error("function getReportData exception. msg: " + str(e))
            return None

    def reportThread(self):
        while True:
            try:
                time.sleep(30)
                mcfg = self.minerargs
                reqData = self.getReportData(mcfg)
                logging.info(' send miner report....')
                logging.info(reqData)
                self.sock.sendall(reqData.encode('utf-8'))
            except Exception as e:
                logging.error("function reportThread exception. msg: " + str(e))

    def downloadWriteFile(self, mcfg):
        while True:
            try:
                req = request.Request(mcfg['minerurl'])
                with request.urlopen(req) as f:
                    with open('./miners/temp.tar.xz', 'wb') as c:
                        c.write(f.read())
                        c.flush()
                        with tarfile.open('./miners/temp.tar.xz') as tar:
                            tar.extractall('./miners')
                            os.remove('./miners/temp.tar.xz')
                            self.minerpath = './miners/' + mcfg['minerver'] + '_linux/' + mcfg['minername']
                            return self.minerpath
            except Exception as e:
                logging.error("function downloadWriteFile exception. msg: " + str(e))
                logging.error('downloadWriteFile failed. sleep 3 seconds.')
                time.sleep(3)

    def checkMinerVer(self, mcfg):
        try:
            mf = './miners/' + mcfg['minerver'] + '_linux'
            if os.path.exists(mf):
                self.minerpath = mf + '/' + mcfg['minername']
                return self.minerpath
            else:
                delcmd = 'rm -rf ./miners/' + mcfg['minerver'].split('_')[0] + '_*'
                os.system(delcmd)
        except Exception as e:
            logging.error("function checkMinerVer exception. msg: " + str(e))
            return None

    def killAllMiners(self, path):
        try:
            cmd = 'ps -x | grep ' + path
            o = os.popen(cmd).read()
            lines = o.splitlines(False)
            for l in lines:
                p = l.lstrip().split(' ')
                if 'grep' in p:
                    continue
                logging.info('kill task pid: ' + p[0])
                os.kill(int(p[0]), signal.SIGKILL)
        except Exception as e:
            logging.error("function killAllMiners exception. msg: " + str(e))
            logging.exception(e)

    def minerThreadProc(self):
        try:
            mcfg = self.minerargs
            if not self.checkMinerVer(mcfg):
                self.downloadWriteFile(mcfg)
            cmd = self.minerpath + ' ' + mcfg['customize']
            process = subprocess.Popen(cmd, shell=True)
            time.sleep(3)
            process.terminate()
            #update miner time
            self.minertime = datetime.now()
        except Exception as e:
            logging.error("function minerThread exception. msg: " + str(e))

    def onGetMinerArgs(self, msg):
        try:
            if 'result' in msg and msg['result']:
                logging.info('get miner args ok.')
                logging.info(msg)

                self.minerargs = msg
                
                #kill miner process, the miner thread will exit
                if self.minerpath:
                    self.killAllMiners(self.minerpath[1:])

                #start new miner thread
                self.mthread = threading.Thread(target=lsminerClient.minerThreadProc, args=(self,))
                self.mthread.start()
                
                #start new report Thread
                if self.rthread == None:
                    self.rthread = threading.Thread(target=lsminerClient.reportThread, args=(self,))
                    self.rthread.start()
            else:
                logging.info('get miner args error. msg: ' + msg['error'])
                q.put(3)
        except Exception as e:
            logging.error("function onGetMinerArgs exception. msg: " + str(e))

    def minerThread(self):
        try:
            mcfg = self.minerargs
            if not self.checkMinerVer(mcfg):
                self.downloadWriteFile(mcfg)

            args = []
            args.append(self.minerpath)
            margs = shlex.split(mcfg['customize'])
            args.extend(margs)
            self.subprocess = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            for line in iter(self.subprocess.stdout.readline, ''):
                print(line.decode('gbk'))
            if self.subprocess.returncode < 0:
                logging.info('miner terminated.')
            else:
                q.put(3)
        except Exception as e:
            logging.error("function minerThread exception. msg: " + str(e))

    def onGetMinerArgsbak(self, msg):
        try:
            if 'result' in msg and msg['result']:
                logging.info('get miner args ok.')

                self.minerargs = msg
                
                #kill miner process, the miner thread will exit
                if self.mthread:
                    while self.mthread.is_alive():
                        if self.subprocess and self.subprocess.poll() == None:
                            #self.subprocess.terminate()
                            self.killAllMiners(self.minerpath[1:])
                        time.sleep(1)

                #start new miner thread
                self.mthread = threading.Thread(target=lsminerClient.minerThread, args=(self,))
                self.mthread.start()
                
                #start new report Thread
                
                if self.rthread == None:
                    self.rthread = threading.Thread(target=lsminerClient.reportThread, args=(self,))
                    self.rthread.start()
            else:
                logging.info('get miner args error. msg: ' + msg['error'])
                q.put(3)
        except Exception as e:
            logging.error("function onGetMinerArgs exception. msg: " + str(e))

    def onReportResp(self, msg):
        pass

    def onUpdateMinerArgs(self, msg):
        logging.info('recv update miner args commond.')
        q.put(3)

    def processMsg(self, msg):
        if 'method' in msg:
            if msg['method'] == 1:
                self.onLoginResp(msg)
            elif msg['method'] == 2:
                self.onGetMinerArgs(msg)
            elif msg['method'] == 3:
                self.onReportResp(msg)
            elif msg['method'] == 4:
                self.onUpdateMinerArgs(msg)
            elif msg['method'] == 5:
                pass
            elif msg['method'] == 6:
                pass
            elif msg['method'] == 7:
                pass
            elif msg['method'] == 8:
                pass
            elif msg['method'] == 9:
                self.onWelcome(msg)
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
                logging.info('unknown server msg method! msg: ' + str(msg))
        else:
            logging.info('unknown server msg! msg: ' + str(msg))


    def recvThread(self):
        try:
            buffer = ''
            while True:
                if self.sock == None:
                    logging.info('client socket == None. sleep 1 second.')
                    time.sleep(1)
                    continue

                buffer += self.sock.recv(4096).decode()
                if '\n' in buffer:
                    msg = json.loads(buffer)
                    self.processMsg(msg)
                    buffer = ''
        except Exception as e:
            logging.info('recvThread exception. msg: ' + str(e))
            time.sleep(1)

    '''cmd list: 1 == connect server, 2 == login server, 3 == get miner config'''
    def processCmd(self, cmd):
        if cmd == 1:
            self.connectSrv()
        elif cmd == 2:
            self.sendLoginReq()
        elif cmd == 3:
            self.sendGetMinerArgsReq()
        elif cmd == 6:
            self.sendLogoutReq()
        else:
            logging.error('unknown cmd. cmd: ' + str(cmd))

    def init(self):
        self.loadCfg()
        thread = threading.Thread(target=lsminerClient.recvThread, args=(self,))
        thread.start()

    def run(self):
        q.put(1)
        while True:
            try:
                cmd = q.get()
                self.processCmd(cmd)
            except Exception as e:
                logging.info("main loop run exception. msg: " + str(e))
                logging.info("sleep 3 seconds and retry...")
                time.sleep(3)


if __name__ == '__main__':
    client = lsminerClient()
    client.init()
    client.run()



    


