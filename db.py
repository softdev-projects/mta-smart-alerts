from pymongo import Connection
from datetime import time


class User(object):
    def __init__(self, name=None, password=None, phone=None, alarm=None):
        """docstring for __init__"""
        pass

    def setEmail(self, name):
        '''string name is an email'''
        self.name = name

    def setPassword(self, password):
        self.password = password

    def setPhone(self, phone):
        """docstring for setPhone"""
        self.phone = phone

    def setAlarm(self, alarm):
        self.alarm = alarm

    def jsonify(self):
        '''returns a Dictionary in Json Format to insert into a mongo db'''
        D = {'name': self.name,
             'password': self.password,
             'phone': self.phone,
             'alarm': self.alarm.jsonify()}
        return D


class Alarm(object):
    def __init__(self, alarmtime, lines):
        '''time time, List of chars for lines'''
        self.alarmtime = alarmtime
        self.lines = lines

    def jsonify(self):
        '''returns a Dictionary in Json Format to insert into a mongo db'''
        D = {'time': self.alarmtime,
             'lines': self.lines}
        return D


def updateUser(user, dbname="users", dbCollectionName="people"):
    success = True

    conn = Connection()
    db = conn[dbname]

    # username/email must have been set so that it can locate the user in the
    # database
    if (not user.name):
        return False
    else:
        pass


def addUser(user, dbname="users", dbCollectionName="people"):
    success = True

    conn = Connection()
    db = conn[dbname]

    if (not isInDatabase(user, dbname, dbCollectionName)):
        jsonUserObject = user.jsonify()
        people = db[dbCollectionName]
        people.insert(jsonUserObject)
    else:
        success = False

    return success


def isInDatabase(user, dbname="users", dbCollectionName="people"):
    '''takes User object, email must have been set'''
    conn = Connection()
    db = conn[dbname]

    # returns a collection of users
    people = db[dbCollectionName]

    success = (people.find({'user': user.name}).count() == 1)

    return success
