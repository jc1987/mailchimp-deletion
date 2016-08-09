from sqlobject import *
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('settings.ini')
sqlhub.processConnection = connectionForURI('mysql://'+config.get('DB', 'username')+':'+config.get('DB', 'password')+'@'+config.get('DB', 'host')+'/'+config.get('DB', 'dbname'))

class Subscriber(SQLObject):
    active = StringCol()
    status = StringCol()
    timestamp_signup = DateTimeCol(default=None)
    member_id = StringCol()
    list_id = IntCol()
    email = StringCol()
    activities_timestamps = StringCol()
    flag = StringCol()