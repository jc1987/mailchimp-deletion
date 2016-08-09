from sqlobject import *
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('settings.ini')
sqlhub.processConnection = connectionForURI('mysql://'+config.get('DB', 'username')+':'+config.get('DB', 'password')+'@'+config.get('DB', 'host')+'/'+config.get('DB', 'dbname'))

class List(SQLObject):
    list_id = StringCol()
    name = StringCol()
