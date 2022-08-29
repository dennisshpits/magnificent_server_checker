import json

# Configuration class encapsulates all logic related to configuration like reading, error checking, etc.
class Configuration:
    port = '12344'
    host = '128.0.0.1'
    url_conn = 'http://' + host + ':' + port
    happy_text = 'happy'
    log_name = 'log.log'
    check_gap = 30 #seconds

    def __init__(self, configpath):
        try:
            with open(configpath) as f:
                data = json.load(f)
        except:
            return

        if self.validport(data['port']):
            self.port = data['port']
        
        self.host = data['host']
        self.happy_text = data['uptext']
        self.log_name = data['logfile']
        self.check_gap = data['check_gap_seconds']
        self.create_url(self.host,self.port)

    def create_url(self,h,p):
        self.url_conn = 'http://' + h + ':' + p

    def validport(self,p):
        try:
            port = int(p)
            if 1 <= port <= 65535:
                return True
            else:
                raise ValueError
        except ValueError:
            return False
    
    def printconfig_logger(self, log):
        try:
            log("port: "+str(self.port))
            log("host: "+str(self.host))
            log("check_timer: "+str(self.check_gap))
            log("url_conn: "+str(self.url_conn))
        except:
            pass