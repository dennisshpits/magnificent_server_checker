import pycurl
from io import BytesIO
import time
import logging

class HealthMonitor:
    crl = pycurl.Curl()
    quit = False
    queue = []

    def __init__(self, configObj):
        self.configurationObject = configObj

        self.logger = logging.getLogger('healthmonitor_logger')
        self.logger.setLevel(level=logging.DEBUG)

        f_handler = logging.FileHandler(self.configurationObject.log_name)
        f_handler.setLevel(logging.DEBUG)
        
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(f_format)

        self.logger.addHandler(f_handler)
        self.crl.setopt(self.crl.URL, self.configurationObject.url_conn)
        self.crl.setopt(self.crl.TIMEOUT, 2)
        self.crl.setopt(self.crl.CONNECTTIMEOUT, 2)

    def __del__(self):
        try:
            self.quit = True
            self.crl.close()
        finally:
            pass

    def stop(self):
        self.quit = True

    def start(self):
        self.logger.debug("starting HealthMonitor")
        self.configurationObject.printconfig_logger(self.logger.debug)
        
        while not self.quit:
            try:
                if (self.serverup()):
                    self.queue.append(1)
                else:
                    self.queue.append(0)
            except Exception as e:
                self.logger.critical(e)
                break

            self.printuptime()
            time.sleep(self.configurationObject.check_gap)
        self.logger.debug("HealthMonitor stopped")

    #send a GET request using pycurl
    def send_get(self):
        b_obj = BytesIO()
        self.crl.setopt(self.crl.WRITEDATA, b_obj)
        
        try:
            self.crl.perform()
        except pycurl.error as e:
            if (e.args[0] == 7): # failed to connect error. We expect this error when the server is down
                pass
            else:
                self.logger.critical("unhandled expection: " + str(e))
            self.logger.warning("Magnificent not responding at all")

        get_body = b_obj.getvalue()
        return get_body.decode('utf8')

    def curlcheck(self):
        if (self.configurationObject.happy_text==self.send_get()):
            return True
        return False

    def serverup(self):
        return self.curlcheck()
    
    def adjust(self):
        #only look at "the last little while"
        while (len(self.queue) > 100):
            self.queue.pop(0)

    def printuptime(self):
        self.logger.info("{0:.0%}".format(float(sum(self.queue))/len(self.queue)))
        self.adjust()