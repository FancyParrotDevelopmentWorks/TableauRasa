
from rasa.api import TableauJSONAPI

SITE_NAME = 'YOUR_SITE_NAME'

#get most visited views

sess = TableauJSONAPI(config_file = 'private_creds.json') #store creds file whereever
sess.auth_signin(SITE_NAME)

view_ct = sess.sites_query_views_for_site(include_usage_stats = True)

views_by_freq_desc = sorted(map(lambda view : [view['contentUrl'], view['name'], int(view['usage']['totalViewCount']) ], view_ct['views']['view']), key = lambda row : -row[2])
# for idx, val in enumerate(views_by_freq_desc):
#     print(idx, val)

users = sess.users_get_users_on_site()
for user in users['users']['user']:
    print(user['name'])

sess.auth_signout()