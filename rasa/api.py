import requests
import json

API_VERSION = 2.5
BASE_HEADER = {
    'accept': 'application/json',
    'content-type': 'application/json'
}


class TableauJSONAPI(object):


    def __init__(self, server_url = None, username = None, password = None, config_file = None):

        if config_file is not None:
            self._set_from_config(config_file)
        else:
            self.server_url = server_url
            self.username = username
            self.password = password

        self.site_url = None
        self.site_id = None
        self.token = None

        self.auth_headers = None

        self.base_url  = "{server_url}/api/{api_version}".format(server_url=self.server_url, api_version=API_VERSION)

    def _set_from_config(self, path):

        data = json.load(open(path, 'rb'))
        self.server_url = data['server_url']
        self.username = data['username']
        self.password = data['password']


    def _get_json(self, url_route):
        url = self.base_url + url_route
        resp = requests.get(url, headers = self.auth_headers)
        resp.raise_for_status()
        return resp.json()

    def _post_json(self, url_route, payload):
        url = self.base_url + url_route
        resp = requests.post(url, headers = self.auth_headers, json=payload)
        resp.raise_for_status()
        return resp.json()



    def _clean_site_name(self, site_name):
        """
        pre processing of site name to Tableau Safe version
        :param site_name:
        :return:
        """
        return site_name.replace(' ', '')

    def auth_signin(self, site_url = ""):

        self.site_url = self._clean_site_name(site_url)

        url_path = self.base_url + '/auth/signin'

        payload = {'credentials':{
            'name': self.username,
            'password': self.password,
            'site': {
                'contentUrl': self.site_url
            }
        }}

        req = requests.post(url_path, json=payload, headers = BASE_HEADER)
        req.raise_for_status()
        resp = json.loads(req.content)

        self.token = resp['credentials']['token']
        self.site_id = resp['credentials']['site']['id']

        self.auth_headers = BASE_HEADER.copy()
        self.auth_headers['X-tableau-auth'] = self.token


        print('Sign in Successful to Site {site_url} {site_url_id}'.format(site_url = self.site_url, site_url_id = self.site_id))

        return self.token

    def auth_signout(self):

        url_path = self.base_url + '/auth/signout'

        req = requests.post(url_path, data = b'', headers = self.auth_headers)
        req.raise_for_status()

        print('Sign Out Successful')
        self.token = None
        self.auth_headers = None
        self.site_id = None
        self.site_url = None
        return None


    def sites_query_site(self, site_url = None):
        """
        :param site_url:
        :return:
        """
        if site_url:
            url_route = '/sites/{site_url}?key=contentUrl'.format(site_url = self._clean_site_name(site_url))
        else:
            url_route = '/sites/{site_id}'.format(site_id  = self.site_id)
        return self._get_json(url_route)


    def sites_query_sites(self):
        return self._get_json(url_route='/sites')


    def sites_query_views_for_site(self, include_usage_stats= False):

        get_usage_information = 'true' if include_usage_stats else 'false'
        url_route = '/sites/{site_id}/views?includeUsageStatistics={get_usage_information}'.format(
            site_id = self.site_id, get_usage_information = get_usage_information)
        return self._get_json(url_route)


    def users_get_users_on_site(self):
        url_route = '/sites/{site_id}/users'.format(site_id = self.site_id)
        return self._get_json(url_route)


    def users_query_user_on_site(self, user_id):
        url_route  = '/sites/{site_id}/users/{user_id}'.format(site_id = self.site_id, user_id = user_id)
        return   self._get_json(url_route)


    def groups_create_group(self, group_name):
        url_route = '/api/api-version/sites/{site_id}/groups'.format(site_id = self.site_id)
        payload = {
            'new-tableau-server-group-name': group_name
        }

        return self._post_json(url_route, payload=payload)


    def get_url(self, url):
        """
        makes an authenticated connection to the specifice url and returns the response object
        :param url:
        :return:
        """

        resp = requests.get(url, cookies = {"workgroup_session_id": self.token})
        resp.raise_for_status()
        return resp




if __name__ == "__main__":

    sess = TableauJSONAPI(config_file='private_creds.json')
    sess.auth_signin(site_url="")
    print(json.dumps(sess.sites_query_views_for_site(include_usage_stats=True), indent=4))
    sess.auth_signout()
