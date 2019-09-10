import time
import os
from lsminer import *

'''循环检测云端指令是否需要重启系统'''
while True:
    try:
        cfg = loadCfg()
        if cfg == 0:
            raise ValueError('loadcfg error!')
        if 'reboot' in cfg:
            url = cfg['reboot'] + getWkid()
        else:
            raise ValueError('config file error!')
        reboot = getReboot(url)
        if reboot:
            print('system will be rebooted')
            os.system("sudo reboot")
        else:
            print('sleep 60 seconds...')
            time.sleep(60)
    except Exception as e:
        print("main loop run exception. msg: " + str(e))
        print("sleep 3 seconds and retry.")
        time.sleep(3)

