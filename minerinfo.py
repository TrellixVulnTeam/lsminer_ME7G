from urllib import request
import time
import socket
import uuid
import json
import os

'''
#define MINER_ID_TREX 1
#define MINER_ID_CCMINER 2
#define MINER_ID_CLAYMORE 3
#define MINER_ID_ZENEMY 4
#define MINER_ID_CRYPTODREDGE 5
#define MINER_ID_XMRIG_N 6
#define MINER_ID_BMINER 7
#define MINER_ID_GMINER 8
#define MINER_ID_EWBF 9 
#define MINER_ID_NBMINER 10 
#define MINER_ID_HSP_BTM 11
#define MINER_ID_HSP_ETH 12 
#define MINER_ID_HSP_AE 13 
#define MINER_ID_SRBMINER 14
#define MINER_ID_WILDRIG 15 
#define MINER_ID_XMRIG_A 16 
#define MINER_ID_LOLMINER 17
#define MINER_ID_GGMINER 18
#define MINER_ID_CCMINER_X20R 19 
#define MINER_ID_CCMINER_MTP 20 
#define MINER_ID_CCMINER_BCX 21 
#define MINER_ID_NBMINER_R 22 
#define MINER_ID_HSP_BEAM 24 
#define MINER_ID_HSP_GRIN 25
#define MINER_ID_TEAMREDMINER 26
#define MINER_ID_SEROMINER_N 28
#define MINER_ID_KBMINER 29 
#define MINER_ID_SEROMINER_A 30

struct DeviceStatusStruc {
 int id = 0;
 string name = "GPU";
 int temp = 0;
 int fan = 0;
 int power = 0;
 float hashrate = 0;
};
struct GPUStatusStruc {
 DeviceStatusStruc* devicestatus;
 int count = 0;
 int uptime = 0;
 float totalhashrate = 0;
 int ts = 0;
};

'''

def getMinerStatus_trex(msdict):
	pass

def getMinerStatus_nbminer(msdict):
	pass

def getMinerStatus_gminer(msdict):
	pass

def getMinerStatus_ewbfminer(msdict):
	pass

def getMinerStatus_bminer(msdict):
	pass

def getMinerStatus_kbminer(msdict):
	pass

def getMinerStatus_hspminer(msdict, aid):
	pass

def getMinerStatus_lolminer(msdict):
	pass

def getMinerStatus_wildrigminer(msdict):
	pass

def getMinerStatus_srbminer(msdict):
	pass

def getMinerStatus_xmrigminer(msdict):
	pass

def getMinerResultDict(url):
	try:
		req = request.Request(url)
		with request.urlopen(req) as f:
			return json.loads(f.read().decode('utf-8'))
	except Exception as e:
		print("function getMinerResult exception. msg: " + str(e))
		return None

def getMinerStatus_url(cfg):
	apimode = cfg['apimode']
	url = cfg['apiurl']
	msdict = getMinerResultDict(url)
	if msdict:
		status = None
		if apimode == 1:
			status = getMinerStatus_trex(msdict)
		elif apimode == 10:
			status = getMinerStatus_nbminer(msdict)
		elif apimode == 8:
			status = getMinerStatus_gminer(msdict)
		elif apimode == 9:
			status = getMinerStatus_ewbfminer(msdict)
		elif apimode == 7:
			status = getMinerStatus_bminer(msdict)
		elif apimode == 29:
			status = getMinerStatus_kbminer(msdict)
		elif apimode == 11:
			status = getMinerStatus_hspminer(msdict, 11)
		elif apimode == 12:
			status = getMinerStatus_hspminer(msdict, 12)
		elif apimode == 13:
			status = getMinerStatus_hspminer(msdict, 13)
		elif apimode == 24:
			status = getMinerStatus_hspminer(msdict, 24)
		elif apimode == 25:
			status = getMinerStatus_hspminer(msdict, 25)
		elif apimode == 17:
			status = getMinerStatus_lolminer(msdict)
		elif apimode == 15:
			status = getMinerStatus_wildrigminer(msdict)
		elif apimode == 14:
			status = getMinerStatus_srbminer(msdict)
		elif apimode == 28:
			status = getMinerStatus_xmrigminer(msdict)
		elif apimode == 30:
			status = getMinerStatus_xmrigminer(msdict)
		return status

	return None

def getMinerResultDict(url):
	cmd = url.split('|')[0] +'\r\n'
	port = url.split('|')[1]
	sock = socket.create_connection(('127.0.0.1', port), 3)
	sock.setblocking(True)
	sock.settimeout(None)
	


def getMinerStatus_tcp(cfg):
	apimode = cfg['apimode']
	url = cfg['apiurl']

def getMinerStatus(cfg):
	apimode = cfg['apimode']
	tcpmode = [3, 4, 5, 26,28, 30]
	if apimode in tcpmode:
		return getMinerStatus_tcp(cfg)
	else:
		return getMinerStatus_url(cfg)
	return None


if __name__ == '__main__':
    pass
