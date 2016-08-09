from sqlobject import *
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('settings.ini')
sqlhub.processConnection = connectionForURI('mysql://'+config.get('DB', 'username')+':'+config.get('DB', 'password')+'@'+config.get('DB', 'host')+'/'+config.get('DB', 'dbname'))

class Activity(SQLObject):
    member_id = StringCol()
    list_id = StringCol()
    action = StringCol()
    timestamp = StringCol()