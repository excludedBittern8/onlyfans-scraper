r"""
               _          __                                                                      
  ___   _ __  | | _   _  / _|  __ _  _ __   ___         ___   ___  _ __   __ _  _ __    ___  _ __ 
 / _ \ | '_ \ | || | | || |_  / _` || '_ \ / __| _____ / __| / __|| '__| / _` || '_ \  / _ \| '__|
| (_) || | | || || |_| ||  _|| (_| || | | |\__ \|_____|\__ \| (__ | |   | (_| || |_) ||  __/| |   
 \___/ |_| |_||_| \__, ||_|   \__,_||_| |_||___/       |___/ \___||_|    \__,_|| .__/  \___||_|   
                  |___/                                                        |_|                
"""
preferences = 'pref_config.py'
configPath = '.config/onlyfans-scraper'
configFile = 'config.json'
authFile = 'auth.json'
databaseFile = 'models.db'
mainProfile = 'main_profile'
requestAuth = 'request_auth.json'
debug = False

# LIST NAMES (IF HARDCODED, MOST WILL BE AUTOMATIC

of_posts_list_name = 'list'

initEP = 'https://onlyfans.com/api2/v2/init'

meEP = 'https://onlyfans.com/api2/v2/users/me'

subscriptionsEP = 'https://onlyfans.com/api2/v2/subscriptions/subscribes?offset={}&type=active&sort=asc&field=expire_date&limit=10'

profileEP = 'https://onlyfans.com/api2/v2/users/{}'

timelineEP = 'https://onlyfans.com/api2/v2/users/{}/posts?limit=100&order=publish_date_desc&skip_users=all&skip_users_dups=1&pinned=0&format=infinite'
timelineNextEP = 'https://onlyfans.com/api2/v2/users/{}/posts?limit=100&order=publish_date_desc&skip_users=all&skip_users_dups=1&beforePublishTime={}&pinned=0&format=infinite'
timelinePinnedEP = 'https://onlyfans.com/api2/v2/users/{}/posts?limit=10&order=publish_date_desc&skip_users=all&skip_users_dups=1&pinned=1&format=infinite'

archivedEP = 'https://onlyfans.com/api2/v2/users/{}/posts/archived?limit=10&order=publish_date_desc&skip_users=all&skip_users_dups=1&format=infinite'
archivedNextEP = 'https://onlyfans.com/api2/v2/users/{}/posts/archived?limit=10&order=publish_date_desc&skip_users=all&skip_users_dups=1&beforePublishTime={}&format=infinite'

highlightsWithStoriesEP = 'https://onlyfans.com/api2/v2/users/{}/stories/highlights?limit=5&offset=0&unf=1'
highlightsWithAStoryEP = 'https://onlyfans.com/api2/v2/users/{}/stories?unf=1'
storyEP = 'https://onlyfans.com/api2/v2/stories/highlights/{}?unf=1'

messagesEP = 'https://onlyfans.com/api2/v2/chats/{}/messages?limit=10&offset=0&order=desc&skip_users=all&skip_users_dups=1'
messagesNextEP = 'https://onlyfans.com/api2/v2/chats/{}/messages?limit=10&offset=0&id={}&order=desc&skip_users=all&skip_users_dups=1'

favoriteEP = 'https://onlyfans.com/api2/v2/posts/{}/favorites/{}'
postURL = 'https://onlyfans.com/{}/{}'

DC_EP = 'https://raw.githubusercontent.com/DATAHOARDERS/dynamic-rules/main/onlyfans.json'

donateEP = "https://www.buymeacoffee.com/taux1c"

purchased_contentEP = "https://onlyfans.com/api2/v2/posts/paid?limit=10&skip_users=all&format=infinite&offset={}"

mainPromptChoices = {
    'Download profile content from a user': 0,
    'Download paid content from a user': 1,
    'Like all of a user\'s posts': 2,
    'Unlike all of a user\'s posts': 3,
    'Migrate an old database': 4,
    'Edit `auth.json` file': 5,
    'Edit `config.json` file': 6,
    'Edit Profile': 7,

}
usernameOrListChoices = {
    'Print a list of my subscriptions': 0,
    'Enter a username': 1,
    'Scrape all users that I\'m subscribed to': 2
}
profilesPromptChoices = {
    'Change profiles': 0,
    'Edit a profile name': 1,
    'Create a profile': 2,
    'Delete a profile': 3,
    'View profiles': 4
}

disclaimers = [
'This tool is not affiliated, associated, or partnered with OnlyFans in any way. We are not authorized, endorsed, or sponsored by OnlyFans. All OnlyFans trademarks remain the property of Fenix International Limited.',
  'This tool is for educational purposes only and is not intended for actual use. Should you choose to actually use it you accept all consequences and agree that you are not using it to redistribute content or  for any other action that will cause loss of revenue to creators or platforms scraped.',
  
  
  
  
  
]

