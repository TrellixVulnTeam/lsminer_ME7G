#!/usr/bin/python3
from tools import *
import os
import sys
import time
from urllib import request
from urllib import parse
import subprocess

import logging

logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt = '%Y-%m-%d  %H:%M:%S %a')


if __name__ == '__main__':
    while True:
        try:
            pass
        except Exception as e:
            logging.error('sendLoginReq exception. msg: ' + str(e))
            logging.exception(e)