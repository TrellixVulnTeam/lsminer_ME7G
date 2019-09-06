# lsminer for linux
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