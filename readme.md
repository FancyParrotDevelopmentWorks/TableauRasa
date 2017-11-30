
#TableauRasa - under development

### Example

```
from rasa.api import TableauJSONAPI


sess = TableauJSONAPI(config_file = 'private_creds.json') #creds is json with un, pw and domain
sess.auth_signin('TableauDevelopers')

view_ct = sess.sites_query_views_for_site(include_usage_stats = True)

views_by_freq_desc = sorted(map(lambda view : [view['contentUrl'], view['name'], int(view['usage']['totalViewCount']) ], view_ct['views']['view']), key = lambda row : -row[2])
    for idx, val in enumerate(views_by_freq_desc):
        print(idx, val)

users = sess.users_get_users_on_site()
    for user in users['users']['user']:
        print(user['name'])

sess.groups_create_group('rasa-test')
sess.script_batch_add_users_to_group(['username'], 'rasa-test')

sess.auth_change_site('sales')

```


# TODO:
 - documentation
 - fill in rest of the api
 
