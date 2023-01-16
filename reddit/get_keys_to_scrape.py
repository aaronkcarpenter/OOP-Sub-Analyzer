import requests
import get_user_agent
import pull_proxy_list
import traceback


class PullAllAfterKeys:
    # user_agent_object = get_user_agent.GetUserAgent()
    # new_user_agent = user_agent_object.random_user_agent()
    proxy_value_obj = pull_proxy_list.PullFreshProxyList()
    # proxy_value = proxy_value_obj.proxySteps()
    # params_get = { 'limit': 100 }
     
    def getAllAfterKeys(self, reddit_authentication_url, proxy_value, user_agent):
        """
        _getAllAfterKeys_
        This function pulls the next 50 after_key strings, puts them in a dictionary. The next function
        which scrapes the page will loop over the keys, replacing the after key in the params after each page
        is scraped.
        """
        try:
            new_after_key = ''
            params_get = { 'limit': 100, 'after': '' }
            afterKeysDict = {}
            requestsMade = 0
            pageNum = 2
            while new_after_key != None and requestsMade < 50:
                req = requests.get(reddit_authentication_url, headers=user_agent, params=params_get, proxies=proxy_value)
                res = req.json()
                new_after_key = res['data']['after']
                params_get['after'] = new_after_key
                
                if new_after_key not in afterKeysDict:
                    afterKeysDict[pageNum] = new_after_key
                    pageNum += 1
                else:
                    continue
                
                if requestsMade % 4 == 0:
                    # proxy_value_obj_new_key_instance = pull_proxy_list.PullFreshProxyList()
                    # proxy_idx = self.proxy_value_obj.new()
                    proxy_value = self.proxy_value_obj.new_proxy_value()
                requestsMade += 1
            print(afterKeysDict)
            return afterKeysDict
        except Exception as e:
            print(f'An error Occurred While Attaining All After Keys --> {e} Line Number: {str(traceback.extract_stack()[-1][1])}')
            
# if __name__ == "__main__":
#     get_after_keys_obj = PullAllAfterKeys()
#     after_key_dict = get_after_keys_obj.getAllAfterKeys()