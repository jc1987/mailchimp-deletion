from mailchimp3 import MailChimp
import ConfigParser
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
from dateutil.relativedelta import relativedelta
from activity import *
from subscriber import *
from list import *
from tqdm import tqdm, trange
import argparse

class Go:
    def __init__(self):
        self.total= 0
        self.alltotal = 0
        self.Config = ConfigParser.ConfigParser()
        self.Config.read('settings.ini')
        self.client = MailChimp(self.Config.get('MailChimp','username'), self.Config.get('MailChimp','key'))

    def compute(self):
        self.listNames = {v.list_id: v.id for v in List.select()}
        self.thresholdDate = datetime.now() + relativedelta(days=-90)
        self.lists = [val for val in self.client.list.all()['lists']]
        for list in self.lists:
            api_response = self.client.member.all(list['id'])
            self.alltotal += int(api_response['total_items'])
        self.tqdmIterator = trange(int(self.alltotal))

        for list in self.lists:
            api_response = self.client.member.all(list['id'])
            for i in range(0, int(api_response['total_items'] / int(self.Config.get('MailChimp', 'items_per_page')))+1):
                api_response = self.client.member.all(list['id'], count=int(self.Config.get('MailChimp', 'items_per_page')),offset=i * int(self.Config.get('MailChimp', 'items_per_page')))
                for member in api_response['members']:
                    self.computeMember(member,list)

    def isOK(self,member,list,activities):
        if(member['status'] =="subscribed"):
            if(any((self.thresholdDate < datetime.strptime(activity['timestamp'][:10], "%Y-%m-%d")) for activity in
            [ac for ac in activities if ac['action'] != "unsub"]) and (len(activities) > 0)):
                return True
            else:
                if(member['timestamp_signup']!=""):
                    if(self.thresholdDate < datetime.strptime(member['timestamp_signup'][0:19], '%Y-%m-%dT%H:%M:%S')):
                        return True

        return False

    def fillLists(self):
        List.deleteMany('id> -1')
        for key, value in {val['name']: val['id'] for val in self.client.list.all()['lists']}.items():
            l =  List(list_id=value, name=key)
            del l

    def computeMember(self,member,list):
        rjson = requests.get('https://us1.api.mailchimp.com/3.0/lists/' + member['list_id'] + '/members/' + member['id'] + '/activity', auth=HTTPBasicAuth(self.Config.get('MailChimp', 'username'),self.Config.get('MailChimp', 'key'))).json()
        activities = rjson['activity']
        for activity in activities:
            a = Activity(member_id=member['id'], list_id=list['id'], action=activity['action'],
                         timestamp=activity['timestamp'])
            del a

        s = Subscriber(
            active="OK" if self.isOK(member, list, activities) else "NOK",
            status=member['status'],
            timestamp_signup=(
            datetime.strptime(member['timestamp_signup'][0:19], '%Y-%m-%dT%H:%M:%S') if member['timestamp_signup'][
                                                                                        0:19] != "" else None),
            member_id=member['id'],
            list_id=self.listNames[list['id']],
            email=member['email_address'],
            activities_timestamps=' '.join([value['timestamp'] for value in activities]) if (
            len(activities) > 0) else " No Activity",
            flag=None)
        del s
        self.tqdmIterator.update(1)

parser = argparse.ArgumentParser()
parser.add_argument('-a','--action', help='what to do fill lists or backup or delete',required=True)

g = Go()
if (parser.parse_args().action=='get_lists'):
    print "FILLING LISTS"
    g.fillLists()
elif (parser.parse_args().action=='backup'):
    print "BACKING UP"
    g.compute()
elif (parser.parse_args().action=='delete'):
    print "DELETION"
else:
    print ""