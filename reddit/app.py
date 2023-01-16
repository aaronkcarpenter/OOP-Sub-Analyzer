import pull_proxy_list
import get_user_agent
import auth_reddit
import request_subreddit_info
import get_keys_to_scrape
import scrape_additional_pages
import scrape_additional_page_v2
import write_filenames_to_text_file

class Scraper:
    """
    Step 1- Getting Proxies to Prevent Blocking
    Step 2 - Getting Authenticated - Saving a variable because we need access to the proxy values and url
    Step 3 - Making The API Requests & Gathering Data
    Step = Pull all After Keys and Stores them in a dictionary, which we return and pass into the next function
    Step - Once we have all after keys, we can loop over the dict and access all needed after keys and continue scraping
    Step 4 - Write/Edit Filenames to Text File and Open Directory
    """
    proxy_instance =  pull_proxy_list.PullFreshProxyList()
    user_agent_object = get_user_agent.GetUserAgent()
    authenticate_reddit_instance = auth_reddit.AuthenticateRedditBot()
    subreddit_scraper_instance = request_subreddit_info.SubredditScraper()
    get_after_keys_obj = get_keys_to_scrape.PullAllAfterKeys()
    additional_page_scraper_instance = scrape_additional_pages.AdditionalPageScraper()
    additional_page_scraper_instance_two = scrape_additional_page_v2.SubRedditScraperAfter()
    write_filenames_to_text_file_instance = write_filenames_to_text_file.WriteFilesToCSV()
    def redditScraper(self):
        """
        We first get the proxies to use that allows us to avoid being rate limited, we then
        all create a user agen object to disguise where we are working from. Once we have
        the proxy and user agent, we pass both into the function that runs to authorize our
        reddit account, getRedditAuth.
        
        Once we've been authenticated, we can make requests to the reddit api with the authenticated
        url, once again passing in a proxy value and a user agent.
        """
        try:
            proxy_value = self.proxy_instance.proxySteps() 
        except Exception as e:
            print(f'There was an error in proxy step {e}')
        try:
            user_agent = self.user_agent_object.random_user_agent()
        except Exception as e:
            print(f'There was an error in user agent class {e}')
        try:
            reddit_authentication_url = self.authenticate_reddit_instance.getRedditAuth(proxy_value, user_agent)
        except Exception as e:
            print(f'There was an error in reddit auth class {e}')
        try:
            requestsToAPI = self.subreddit_scraper_instance.makeRequestsToAPI(reddit_authentication_url, proxy_value, user_agent)
            try:
                # after_key_dict = self.get_after_keys_obj.getAllAfterKeys(reddit_authentication_url, proxy_value, user_agent)
                scrape_the_rest = self.additional_page_scraper_instance_two.scrape_after_first_100(reddit_authentication_url, proxy_value, user_agent, requestsToAPI)
            except Exception as e:
                print(f'There was an error in reddit requests additional pages scraper class {e}') 
        except Exception as e:
            print(f'There was an error in reddit requests scraper class {e}')
        # try:
        #     after_key_dict = self.get_after_keys_obj.getAllAfterKeys(reddit_authentication_url, proxy_value, user_agent)
        # except Exception as e:
        #     print(f'There was an error in main {e}')
        # try:
        #     additional_page_scraper = self.additional_page_scraper_instance.scrapeAdditionalPages(reddit_authentication_url, proxy_value, after_key_dict, user_agent)
        # except Exception as e:
        #     print(f'There was an error in main {e}')
        # try:
        #     write_to_csv = self.write_filenames_to_text_file_instance.writeFileNamesToTextFile()
        # except Exception as e:
        #     print(f'There was an error in main {e}')
        # try:
        #     awsCreds = connectAndUpload()
        # except Exception as e:
        #     print(f'There was an error in main {e}')
        
if __name__ == '__main__':
    scraper_instance = Scraper()
    run_scraper = scraper_instance.redditScraper()
    
# 1 Get list of proxies to use
# 2 Get Reddit Authorization
# Make Request to Get First page Data Scraped
# Connect to AWS
# Upload first page media to S3
# Get the after key for 50 max pages to scrape and save in a dict - getAllAfterKeys()
# Scrape the additional pages --> I have 50 after keys available
# upload to s3 after each page is scraped
# Add the saved/uploaded media url's to a completed set
# If at the last page of scraping, add the url's to the files captured text file
# break