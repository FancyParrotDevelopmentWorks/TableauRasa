

from rasa.api import TableauJSONAPI
import unittest


class TestConnection(unittest.TestCase):

    def setUp(self):
        self.sess = TableauJSONAPI(config_file = 'private_creds.json')
        self.sess.auth_signin('TableauDevelopers')


    def test_has_sites(self):
        print self.sess.sites_query_sites()['pagination']['totalAvailable']
        self.assertGreater(int(self.sess.sites_query_sites()['pagination']['totalAvailable']), 0, 'should get something here')


    def tearDown(self):
        self.sess.auth_signout()

class TestAddUser(unittest.TestCase):
    pass

class TestAddGroup(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main(verbosity=2)