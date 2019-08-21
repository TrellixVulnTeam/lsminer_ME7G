import time
import os
from lsminer import *

'''循环检测云端指令是否需要重启系统'''
while True:
    try:
        cfg = loadCfg()
        url = cfg['reboot'] + md5(getMac())
        reboot = getReboot(url)
        if reboot:
            os.system("reboot")
        else:
            time.sleep(60)
    except Exception as e:
        print("main loop run exception. msg: " + str(e))
        print("sleep 3 second and retry.")
        time.sleep(3)

