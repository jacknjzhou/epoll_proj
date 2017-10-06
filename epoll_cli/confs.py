#!-*-coding:utf8-*-
import ConfigParser
import os

class Config(object):
    
    def __init__(self,conf_file):
        self.conf_file = conf_file
        self.cf = self._open_conf()
        print self.cf.sections()
    
    def _open_conf(self):
        cf = ConfigParser.ConfigParser()
        cf.read(self.conf_file)
        return cf 

    def get(self, section, option,default=None):
        """function:get section-->option value"""
        try:
            return self.cf.get(section,option)

        except:
            return default

if __name__ =='__main__':
    conf_obj = Config('client.ini')
    ip = conf_obj.get('SERVER','server.ip','')
    port = conf_obj.get('SERVER','server.port','18888')

    print ip
    print port
