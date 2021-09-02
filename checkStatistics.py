import configparser
import os

config = configparser.ConfigParser()

config.read(os.path.dirname(os.path.abspath(__file__))+"/../config/statistics.ini")

for section_name in config.sections():
    print ('\n%s' %section_name)
    for name, value in sorted(config.items(section_name)):
        print ('  %s = %s' % (name, value))
    print