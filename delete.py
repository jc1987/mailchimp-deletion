from mailchimp3 import MailChimp
import ConfigParser
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
from dateutil.relativedelta import relativedelta
from activity import *
from subscriber import *
from tqdm import tqdm, trange
import csv

class Del:
    def __init__(self):
        self.total= 0
        self.leftovers = []
        self.Config = ConfigParser.ConfigParser()
        self.Config.read('settings.ini')
        self.client = MailChimp(self.Config.get('MailChimp','username'), self.Config.get('MailChimp','key'))

    def compute(self):
        for leftover in self.leftovers:
            #self.deleteMember("balbalbalablablabalalalabalbalal",leftover)
            print leftover+ " deleted"

    def deleteMember(self,list_id,member_id):
        self.client.member.delete(list_id=list_id, member_id=member_id)

g = Del()
g.compute()
