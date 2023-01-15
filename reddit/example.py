import get_user_agent
import pull_proxy_list
import os
import requests
from fake_useragent import UserAgent
from requests.auth import HTTPBasicAuth


class Scraper:
    
    ua = UserAgent()
    user_agent = get_user_agent.random_user_agent()
    proxy_value = pull_proxy_list.proxySteps()
    auth_creds = HTTPBasicAuth(os.environ.get('REDDIT_CLIENT_ID'), os.environ.get('REDDIT_CLIENT_SECRET'))
    post_data = {'grant_type': 'password', 'username':os.environ.get('REDDIT_USERNAME'), 'password': os.environ.get('REDDIT_PASSWORD')}
    TOKEN_ACCESS_ENDPOINT='https://www.reddit.com/api/v1/access_token'
    OAUTH_ENDPOINT_PREFIX = f'https://oauth.reddit.com'
    
    def __init__(self):
        pass
    
    def authenticate_user(self):
        try:
            res = requests.post(self.TOKEN_ACCESS_ENDPOINT, data=self.post_data, headers=self.user_agent, auth=self.auth_Creds, proxies=self.proxy_value)
            if res.status_code == 200:
                token_id = res.json()['access_token'] # have to add into header when making requests
                self.user_agent['Authorization'] = f'Bearer {token_id}'
                finalAuthUrl = f'{self.OAUTH_ENDPOINT_PREFIX}{self.baseUrl}'
                print(f'Reddit Authentication Was A Success, auth_reddit.py is the function and the reddit auth url is {finalAuthUrl}')
                return finalAuthUrl
        except Exception as e:
            print(f'Ran into an authentication issue {e}')
        
        
if __name__ == "__main__":
    scraper_instance = Scraper()
    scraper_instance.authenticate_user()