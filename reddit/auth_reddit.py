import get_user_agent
import pull_proxy_list
import os
import random
import requests
from requests.auth import HTTPBasicAuth

class AuthenticateRedditBot:
    # proxy_value_instance = pull_proxy_list.PullFreshProxyList()
    # proxy_value = proxy_value_instance.pullRandomProxy()
    # user_agent_instance = get_user_agent.GetUserAgent()
    # user_agent = user_agent_instance.random_user_agent()
    auth_Creds = HTTPBasicAuth(os.environ.get('REDDIT_CLIENT_ID'), os.environ.get('REDDIT_CLIENT_SECRET'))
    post_data = {'grant_type': 'password', 'username':os.environ.get('REDDIT_USERNAME'), 'password': os.environ.get('REDDIT_PASSWORD')}
    TOKEN_ACCESS_ENDPOINT='https://www.reddit.com/api/v1/access_token'
    OAUTH_ENDPOINT_PREFIX = f'https://oauth.reddit.com'
    limit = 100
    timeframe = 'all'
    listing = 'top'
    # baseUrl = 'https://oauth.reddit.com/r/python/hot'
    baseUrl = f'/r/{subreddit}/{listing}?t={timeframe}'
            
    def getRedditAuth(self, proxy_value, user_agent):
        """
            Step 2 - Get Authorization from Reddit to Make Requests
            Make a POST request to the token access endpoint
            if successful, save the token to the token id variable
            save that token id in the userAgentDict that is used later
            now that we have all needed data, we can start making requests
        """
        try:
            res = requests.post(self.TOKEN_ACCESS_ENDPOINT, data=self.post_data, headers=user_agent, auth=self.auth_Creds, proxies=proxy_value)
            if res.status_code == 200:
                token_id = res.json()['access_token']
                user_agent['Authorization'] = f'Bearer {token_id}'
                finalAuthUrl = f'{self.OAUTH_ENDPOINT_PREFIX}{self.baseUrl}'
                return finalAuthUrl
        except Exception as e:
            print(f'Ran into an authentication issue {e}')

# if __name__ == "__main__":
#     authenticate_reddit_instance = AuthenticateRedditBot()
    