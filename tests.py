

from rasa.api import TableauJSONAPI
import unittest
import time


class Base(unittest.TestCase):

    def setUp(self):
        time.sleep(0.5) #so you're not killing the server
        self.sess = TableauJSONAPI(config_file = 'private_creds.json')
        self.sess.auth_signin('TableauDevelopers')


    def tearDown(self):
        self.sess.auth_signout()


class TestConnection(Base):

    def test_has_sites(self):
        self.assertGreater(int(self.sess.sites_query_sites()['pagination']['totalAvailable']), 0, 'should get something here')


class TestGetWorks(Base):
    """
    Just starting off testing all get commands dont throw coding errors
    """

    def test_sites_query_site(self):
        self.assertIn('site', self.sess.sites_query_site())

    def test_sites_query_views_for_site(self):
        self.assertIn('views', self.sess.sites_query_views_for_site())

    def test_workbooks_query_workbooks_for_sites(self):
        self.assertIn('workbooks', self.sess.workbooks_query_workbooks_for_sites())

    def test_users_get_users_on_site(self):
        self.assertIn('users', self.sess.users_get_users_on_site())

    def test_users_query_user_on_site(self):
        uid = self.sess.users_get_users_on_site()['users']['user'][0]['id']
        self.assertIsNotNone('user', self.sess.users_query_user_on_site(uid))



# class TestAddUser(unittest.TestCase):
#     pass
#
# class TestAddGroup(unittest.TestCase):
#     pass


if __name__ == '__main__':
    unittest.main(verbosity=2)