import unittest
import db
import datetime
from pymongo import Connection

collectionName = "testdatabase"
dbname = "testdb"


class defaultTest(unittest.TestCase):
    """Class for default setUp and tearDown methods for testing"""
    def setUp(self,
              names=["1", "2", "3"],
              dbname="testdb",
              collectionName="testdatabase"):

        self.dbname = dbname
        self.dbCollectionName = collectionName
        self.names = names
        self.conn = Connection()
        self.db = self.conn[dbname]

    def tearDown(self):
        self.db.testdatabase.drop()


class testAlarmClassAndUserClass(defaultTest):
    def test_jsonify_alarm(self):
        testTime = datetime.datetime(2014, 1, 1, 0, 0)
        lines = ["1", "2", "3", "4", "A", "B", "C"]

        alarm = db.Alarm(testTime, lines)

        D = alarm.jsonify()

        self.assertDictEqual(D,
                             {'time': datetime.datetime(2014, 1, 1, 0, 0),
                              'lines': lines})

    def test_jsonify_user(self):
        name = "testname"
        password = "testpassword"
        phone = "1111111111"
        authenticated = True

        time = datetime.datetime(year=2014, month=1, day=1, hour=0, minute=0)
        lines = ["1", "2", "3", "4", "A", "B", "C"]
        alarm = db.Alarm(time, lines)

        user = db.User(name)
        user.setPassword(password)
        user.setPhone(phone)
        user.setAuthenticated(authenticated)
        user.setAlarm(alarm)

        D = user.jsonify()

        D2 = {'name': name,
              'password': password,
              'phone': phone,
              'authenticated': authenticated,
              'alarm': {'time': time,
                        'lines': lines}}

        self.assertDictEqual(D, D2)

    def test_insert(self):
        time = datetime.datetime(year=2014, month=1, day=1, hour=0, minute=0)
        alarm = db.Alarm(time, ["1", "2", "3"])

        user = db.User("testuser1")
        user.setPassword("testuser1password")
        user.setAlarm(alarm)
        user.setAuthenticated(True)
        user.setPhone("1111111111")

        success = db.addUser(user, self.dbname, self.dbCollectionName)
        self.assertEquals(success, True)

        # check if it's actually in the database
        conn = Connection()
        mongodb = conn[self.dbname]

        people = mongodb[self.dbCollectionName]

        num = people.find({'name': user.name}).count()
        inserted = num == 1

        self.assertEquals(True, inserted)

    def test_update_user(self):
        time = datetime.datetime(year=2014, month=1, day=1, hour=0, minute=0)
        alarm = db.Alarm(time, ["1"])

        conn = Connection()
        mongodb = conn[self.dbname]
        people = mongodb[self.dbCollectionName]

        # insert a lot of users into the database
        for i in range(10):
            user = db.User("testuser%d" % i)
            user.setPassword("testpassword%d" % i)
            user.setAlarm(alarm)
            user.setAuthenticated(False)
            user.setPhone("111111111%d" % i)

            people.insert(user.jsonify())

        # change all the users to the same values
        newtime = datetime.datetime(year=2014, month=1, day=1, hour=5, minute=5)
        newlines = ["1", "2", "3"]
        newalarm = db.Alarm(newtime, newlines)
        newpassword = "newpassword"
        newAuth = True
        newPhone = "1231231234"

        for user in people.find():
            newuser = db.User(user['name'])
            newuser.setPassword(newpassword)
            newuser.setAlarm(newalarm)
            newuser.setAuthenticated(newAuth)
            newuser.setPhone(newPhone)

            db.updateUser(newuser, self.dbname, self.dbCollectionName)

        # count the number of each attribute
        L = []
        L.append(people.find({'password': newpassword}).count())
        L.append(people.find({'authenticated': newAuth}).count())
        L.append(people.find({'phone': newPhone}).count())
        L.append(people.find({'alarm': {'time': newtime,
                                        'lines': newlines}}).count())

        # each element should be 10
        for n in L:
            self.assertEquals(n == 10, True)


def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(
        testAlarmClassAndUserClass)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    main()
