import get_user_agent 
import random
import requests
from bs4 import BeautifulSoup

class PullFreshProxyList:
    
    user_agent_object = get_user_agent.GetUserAgent()
    new_user_agent = user_agent_object.random_user_agent()
    proxyUrl = f'https://www.sslproxies.org/'
    proxies = [] # stores the list of dicts. Each dict has an ip and port
    
    def proxySteps(self):
        """_proxySteps_
            Get The Latest Proxies
            Making a request to sslproxies to get the latest, parsing the ip addresses from the table,
            and saving the ip and port as two values to each key. There will be a dictionary/object for each row in the proxies 
            list/array. We then call the pullRandomProxy function to get the index of an available proxy
            in the list

            Step 1 - Getting and Populating the List of Proxies
            Call proxySteps func to get the latest ip addresses from the table
            Saving a random user agent string in the dict that is passed into our proxy request to the sslproxies site
            Open the req to examine and parse the data from the table that was found
            Loop each row of the table and append them to the proxies list/array
            Otherwise return the error associated with not being able to get the latest proxies
        """
        try:
            proxiesReq = requests.get(self.proxyUrl, headers=self.new_user_agent)
            soup = BeautifulSoup(proxiesReq.text, 'html.parser')
            proxiesTable = soup.find("table", class_='table')
            
            # Looping the Proxy Table to Save the Latest Proxies
            for row in proxiesTable.tbody.find_all('tr'):
                self.proxies.append({
                    'ip': row.find_all('td')[0].string,
                    'port': row.find_all('td')[1].string
                })
                
            # Select a Random Proxy from the List of Proxies by calling pullRandomProxy() 
            # We then access the proxy dict at the index we randomly pulled, and return it
            # To give access to the proxy values in the main func
            proxy_idx = self.pullRandomProxy()
            proxy = self.proxies[proxy_idx]
            return proxy
        except Exception as e:
            print(f'A problem occurred in ProxySteps: {e}')  
            
    def pullRandomProxy(self):
        """_pullRandomProxy
            Returns the index of a random proxy from the proxy array of dicts,
            returning the key, not the value. Just in case there is no proxy,
            we have the index(key) and delete it.
        """
        return random.randint(0, len(self.proxies) - 1)
    
# if __name__ == "__main__":
#     proxy_instance_obj =  PullFreshProxyList()
#     proxy_obj = proxy_instance_obj.proxySteps()    