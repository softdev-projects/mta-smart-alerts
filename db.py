from pymongo import Connection


class User(object):
    def __init__(self, name):
        """must take a string as the username"""
        self.name = name

    def setName(self, name):
        '''string name, is the user's email or username'''
        self.name = name

    def setPassword(self, password):
        '''string password'''
        self.password = password

    def setPhone(self, phone):
        """string phone number, ONLY NUMBERS PLEASE"""
        self.phone = phone

    def setAlarm(self, alarm):
        '''class Alarm'''
        self.alarm = alarm

    def setAuthenticated(self, isAuthenticated):
        '''boolean isAuthenticated'''
        self.authenticated = isAuthenticated

    def jsonify(self):
        '''returns a Dictionary in Json Format to insert into a mongo db'''
        D = {'name': self.name,
             'password': self.password,
             'phone': self.phone,
             'authenticated': self.authenticated,
             'alarm': self.alarm.jsonify()}
        return D


class Alarm(object):
    '''Object that contains the lines that the user wants to be alerted for
    and the time that they want to be alerted'''
    def __init__(self, alarmtime, lines):
        '''datetime alarmtime, List of chars for lines'''
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
        success = False
    else:
        D = user.jsonify()

        if (isInDatabase(user, dbname, dbCollectionName)):
            people = db[dbCollectionName]

            for key, value in D.iteritems():
                if value is not None:
                    people.update({'name': user.name},
                                  {"$set": {key: value}},
                                  upsert=False)
        else:
            success = False

    return success


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

    success = (people.find({'name': user.name}).count() >= 1)

    return success