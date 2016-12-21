from configparser import ConfigParser
import os

class Config:
    def __init__(self):
        self.config_path = os.path.join(os.environ['HOME'], '.build.cfg')
        self.parser = ConfigParser()
        try:
            self.parser.read(self.config_path)
        except:
            import sys
            print("WARNING: Can't read config %s" % self.config_path, file=sys.stderr)
    def get(self, arg, default=None):
        try:
            return self.parser.get('COMMON', arg)
        except:
            return default
