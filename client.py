#!/usr/bin/python3
from signal import signal, SIGINT, SIGTERM
from sys import exit
from concurrent.futures import ThreadPoolExecutor
from modules.configmod import Configuration
from modules.healthcheckermod import HealthMonitor
import time

quit = False # quit used to notify thread functions to exit

def handler(signal_received, frame):
    global quit
    quit = True

def run():
    signal(SIGINT, handler)
    signal(SIGTERM, handler)
    configObj = Configuration('config.json')
    HMonitorObj = HealthMonitor(configObj)

    #start executors
    executor = ThreadPoolExecutor(max_workers=1)
    hmfut = executor.submit(HMonitorObj.start)

    global quit
    while(not quit):#wait until SIGINT or SIGTERM detected
        time.sleep(2)

    HMonitorObj.stop()

    while(not hmfut.done()): # wait until future is done
        time.sleep(1)

if __name__ == "__main__":
    run()