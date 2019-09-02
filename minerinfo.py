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
	try:
		minerstatus = {}
		minerstatus['uptime'] = msdict['uptime']
		minerstatus['hashrate'] = []
		for device in msdict['gpus']:
			minerstatus['hashrate'].append(device['hashrate'])
			minerstatus['totalhashrate'] += device['hashrate']
		return minerstatus
	except Exception as e:
		print("function getMinerStatus_trex exception. msg: " + str(e))
		return None
	return None

def getMinerStatus_nbminer(msdict):
	try:
		minerstatus = {}
		minerstatus['uptime'] = 0
		minerstatus['hashrate'] = []
		for device in msdict['miner']['devices']:
			minerstatus['hashrate'].append(device['hashrate_raw'])
			minerstatus['totalhashrate'] += device['hashrate_raw']
		return minerstatus
	except Exception as e:
		print("function getMinerStatus_nbminer exception. msg: " + str(e))
		return None
	return None

def getMinerStatus_gminer(msdict):
	try:
		minerstatus = {}
		minerstatus['uptime'] = msdict['uptime']
		minerstatus['hashrate'] = []
		for device in msdict['devices']:
			minerstatus['hashrate'].append(device['speed'])
			minerstatus['totalhashrate'] += device['speed']
		return minerstatus
	except Exception as e:
		print("function getMinerStatus_gminer exception. msg: " + str(e))
		return None
	return None

def getMinerStatus_ewbfminer(msdict):
	try:
		minerstatus = {}
		minerstatus['uptime'] = 0
		minerstatus['hashrate'] = []
		for device in msdict['result']:
			minerstatus['hashrate'].append(device['speed_sps'])
			minerstatus['totalhashrate'] += device['speed_sps']
		return minerstatus
	except Exception as e:
		print("function getMinerStatus_ewbfminer exception. msg: " + str(e))
		return None
	return None

def getMinerStatus_bminer(msdict):
	try:
		minerstatus = {}
		minerstatus['uptime'] = 0
		minerstatus['hashrate'] = []
		for device in msdict['miners'].values():
			minerstatus['hashrate'].append(device['solver']['solution_rate'])
			minerstatus['totalhashrate'] += device['solver']['solution_rate']
		return minerstatus
	except Exception as e:
		print("function getMinerStatus_bminer exception. msg: " + str(e))
		return None
	return None

def getMinerStatus_kbminer(msdict):
	return None

def getMinerStatus_hspminer(msdict, aid):
	return None

def getMinerStatus_lolminer(msdict):
	return None

def getMinerStatus_wildrigminer(msdict):
	return None

def getMinerStatus_srbminer(msdict):
	return None

def getMinerStatus_xmrigminer(msdict):
	return None

#tcp

def getMinerStatus_claymoreminer(msdict):
	return None

def getMinerStatus_CryptoDredgeMiner(buf):
	return None

def getMinerStatus_TeamRedMiner(buf):
	return None

def getMinerStatus_ZEnemyMiner(buf):
	return None

def getMinerResultDict_url(url):
	try:
		req = request.Request(url)
		with request.urlopen(req) as f:
			return json.loads(f.read().decode('utf-8'))
	except Exception as e:
		print("function getMinerResultDict_url exception. msg: " + str(e))
		return None

def getMinerStatus_url(cfg):
	apimode = cfg['apimode']
	url = cfg['apiurl']
	msdict = getMinerResultDict_url(url)
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

def getMinerResult_tcp(url):
	try:
		cmd = url.split('|')[0] +'\r\n'
		port = url.split('|')[1]
		sock = socket.create_connection(('127.0.0.1', port), 3)
		sock.setblocking(True)
		sock.settimeout(None)
		sock.sendall(cmd.encode())
		buf = sock.recv(10240).decode()
		sock.close()
		return buf
	except Exception as e:
		print("function getMinerResultDict_tcp exception. msg: " + str(e))
		return None

def getMinerStatus_tcp(cfg):
	apimode = cfg['apimode']
	url = cfg['apiurl']
	buf = getMinerResult_tcp(url)
	if buf:
		status = None
		if apimode == 4:
			status = getMinerStatus_ZEnemyMiner(buf)
		elif apimode == 5:
			status = getMinerStatus_CryptoDredgeMiner(buf)
		elif apimode == 26:
			status = getMinerStatus_TeamRedMiner(buf)
		elif apimode == 3 or apimode == 28 or apimode == 30:
			msdict = json.loads(buf)
			status = getMinerStatus_claymoreminer(msdict)
		return status
	return None


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
