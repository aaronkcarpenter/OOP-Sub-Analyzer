from datetime import datetime
import add_saved_media
import get_user_agent
import pull_proxy_list
import auth_reddit
import remove_saved_media
import write_filenames_to_text_file
import get_keys_to_scrape
import os
import requests
import traceback
from bs4 import BeautifulSoup
from datetime import datetime


class SubredditScraper:
    
    # reddit_authentication_obj = auth_reddit.AuthenticateRedditBot()
    # reddit_authentication_url = reddit_authentication_obj.getRedditAuth()
    # proxy_value_obj = pull_proxy_list.PullFreshProxyList()
    # proxy_value = proxy_value_obj.proxySteps()
    # user_agent_object = get_user_agent.GetUserAgent()
    # new_user_agent = user_agent_object.random_user_agent()
    # remove_saved_media_obj = remove_saved_media.MediaCleaning()
    # remove_media  = remove_saved_media_obj.removeSavedMedia()
    media_saving_instance = add_saved_media.AddMedia()
    # add_media = media_saving_instance.addSavedMediaToCompleted()
    get_after_keys_obj = get_keys_to_scrape.PullAllAfterKeys()
    # after_key_dict = get_after_keys_obj.getAllAfterKeys()
    # filename_to_csv_instance = write_filenames_to_text_file.WriteFilesToCSV()
    # write_to_csv = filename_to_csv_instance.writeFileNamesToTextFile()
    
    # subreddit = 'BlackPeopleTwitter'
    subreddit = 'JaydaWayda'
    # subreddit = 'ZsTittyTreats'
    # subreddit = 'HipHopGoneWild'
    limit = 100
    timeframe = 'all'
    # listing = 'top'
    listing = 'year'
    params_get = { 'limit': 100 }
    baseUrl = f'/r/{subreddit}/{listing}?t={timeframe}'
    now = datetime.now()
    now_folder = datetime.today()
    redditImgDirectory = '/Users/aaroncarpenter/Desktop/Programming/Projects/bots/send_tweet_with_media_bot/reddit/images/'
    path = f'{redditImgDirectory}{subreddit}/{now_folder}'
    redditVideoDirectory = '/Users/aaroncarpenter/Desktop/Programming/Projects/bots/send_tweet_with_media_bot/reddit/videos/'
    completedMedia = set()
    mediaAddedDict = {}
    
    # def __init__(self, reddit_authentication_url: str, proxy_value: str, user_agent: dict) -> None:
    #     self.reddit_authentication_url = reddit_authentication_url
    #     self.proxy_value = proxy_value
    #     self.user_agent = user_agent
    
    def makeRequestsToAPI(self, reddit_authentication_url, proxy_value, user_agent):
        """
        Outerloop loops 10 times & each request includes 100 posts(outerloop).For every 10 requests made to the reddit api,
        get a new proxy. This is to avoid being blocked from the api and allows us to make more than 100 requests, which is an API limitation.
        
        Step 3- Making Requests to the API
        In the main func, Set the url to the endpoint/api i'll be making the requests to
        Loop over the range of 1 to 101 as we will be making 100 requests/10,000 Posts
        Using the requests package, we make a request and pass in a random proxy from step 1
        Every 10 requests we get a new proxy from the list of proxies by calling the pullRandomProxy function and get the proxyValue from the idx chosen
        Make a request to the api and print the IP, if this works, things are working well, otherwise we have a bad proxy
        """
        try:
            req = requests.get(reddit_authentication_url, headers=user_agent, params=self.params_get, proxies=proxy_value)
            res = req.json()
            posts = res['data']['children'] # where are the good data lives
            post_titles = []
            after_key = res['data']['after']
            before_key = res['data']['before']
            
            """
            Accessing the large images for each post being pulled,
            saving into 'postImages'. Image Counter allows us to dynamically
            change the picture as we save each one by incrementing after each save.
            
            The first inner for loop iterates through the posts key in the response
            which should have 100 total per request. Saving the post title and image,
            if the post picture isn't in the set of completed images that have already
            been processed and seen, we want to save the image url and set the title
            for the post.
            
            The 2nd inner loop is where we save each file that we appended in the first
            inner for loop.
            """
            listOfImageFiles = os.listdir(self.redditImgDirectory)
            postData = {}
            pulledPostImageUrls = []
            for j in range(len(posts)):
                post_data_available = posts[j]['data'].keys()
                postTitle =  posts[j]['data']['title']
                
                if posts[j]['data'].get('url_overridden_by_dest') == None:
                    continue
                post_image_url = posts[j]['data']['url_overridden_by_dest']
                
                postImage = None
                post_title = posts[j]['data']['title']
                post_url = posts[j]['data']['url']
                post_creation_time_unix = posts[j]['data']['created_utc']
                post_creation_time_readable = datetime.fromtimestamp(post_creation_time_unix)
                subreddit_name = posts[j]['data']['subreddit']
                subreddit_subscribers = posts[j]['data']['subreddit_subscribers']
                upvotes_ratio = posts[j]['data']['upvote_ratio']
                post_upvotes = posts[j]['data']['ups']
                post_downvotes = posts[j]['data']['downs']
                post_score = posts[j]['data']['score']
                print(post_title, post_url, post_creation_time_readable, subreddit_name, subreddit_subscribers, upvotes_ratio, post_upvotes, post_downvotes, post_score)
                
                post_titles.append(post_title)
                
                if posts[j]['data'].get('url_overridden_by_dest') == None:
                    continue
                
                galleryURL = 'gallery'
                if galleryURL in post_image_url:
                    continue
                
                post_image_urls = posts
                postVideoURL = 'v.redd.it'
                postImageURL = 'i.redd.it'
                if postVideoURL in post_image_url:
                    postImage = post_image_urls[j]['data']['secure_media']['reddit_video']['fallback_url']
                elif postImageURL in post_image_url:
                    postImage = post_image_urls[j]['data']['url_overridden_by_dest']
                
                if postImage not in self.completedMedia:
                    pulledPostImageUrls.append(postImage)
                    postData[postTitle] = [postImage, self.now]
                    
            mediaCounter = len(listOfImageFiles) + 1
            reqPicContent = []
            reqPicFileName = []
            for k in range(0, len(pulledPostImageUrls)):
                currentMedia = pulledPostImageUrls[k]
                if currentMedia != None:
                    mediaDictCount = len(self.mediaAddedDict)
                    self.mediaAddedDict[mediaDictCount + 1] = [self.now, currentMedia]
                    
                    if postVideoURL in currentMedia:
                        postMediaType = 'mp4'
                        # fileBeingSaved = f'{self.redditVideoDirectory}/reddit_Video_{self.subreddit}_{mediaCounter}.{postMediaType}'
                        fileBeingSaved = f'{self.path}/reddit_Video_{self.subreddit}_{mediaCounter}.{postMediaType}'
                        fileName = f'reddit_Video_{self.subreddit}_{mediaCounter}.{postMediaType}'
                        reqPicFileName.append(fileName)
                    elif postImageURL in currentMedia or galleryURL in currentMedia:
                        postMediaType = 'jpg'
                        # fileBeingSaved = f'{self.redditImgDirectory}/reddit_Image_{self.subreddit}_{mediaCounter}.{postMediaType}'
                        fileBeingSaved = f'{self.path}/reddit_Image_{self.subreddit}_{mediaCounter}.{postMediaType}'
                        fileName = f'reddit_Image_{self.subreddit}_{mediaCounter}.{postMediaType}'
                        reqPicFileName.append(fileName)
                    
                    reqPicData = requests.get(currentMedia).content
                    reqPicContent.append(fileBeingSaved)
                    
                    if not os.path.exists(self.path):
                        os.makedirs(self.path)
                        
                    with open(os.path.join(self.path, fileBeingSaved), 'wb') as f:
                        f.write(reqPicData)
                        
                    # with open(f'{fileBeingSaved}', 'wb') as f:
                    #     f.write(reqPicData)
                    mediaCounter += 1
                    print(f'Which file was saved? {fileBeingSaved}')
                else:
                    continue
                
                if k == j:
                    # awsConnection.uploadToS3(reqPicContent, reqPicFileName) # uncomment when I have everything figured out to avoid s3
                    self.media_saving_instance.addSavedMediaToCompleted(pulledPostImageUrls)
                
                print('End of First Page Scrape, 1st scrape uploading, media saved, Get the After keys Now...')
                
            if len(after_key) != 0:
                self.get_after_keys_obj.getAllAfterKeys(reddit_authentication_url, proxy_value, user_agent)
                
            print(f'How Many Saved Images Thus Far? {len(listOfImageFiles)}')
            print(len(posts))
            soup = BeautifulSoup(req.text, 'html.parser')
            
            # Do I have all the data that I wanted? If so, time to make another request with a new proxy and 100 more posts
            # Call pullRandomProxy Get a new Proxy every 10 requests from the proxies current list of dicts
            # if i % 10 == 0:
            #     proxy_idx = pullRandomProxy()
            #     proxyValue = proxies[proxy_idx]  
                
                    # scrapeAdditionalPages(scrapingUrl, proxyValue, after_key)
            # return redditImgDirectory
            # return req.json()
        except Exception as e:
            print(f'An error Occurred In The Request Function! --> {e} Line Number: {str(traceback.extract_stack()[-1][1])}')
            
# if __name__ == "__main__":
#     subreddit_scraper_instance = SubredditScraper()
    