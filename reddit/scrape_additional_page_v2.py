from datetime import datetime
import auth_reddit
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

class SubRedditScraperAfter:
    
    now = datetime.now()
    media_saving_instance = add_saved_media.AddMedia()
    subreddit = 'BeachInspo'
    limit = 100
    timeframe = 'all'
    listing = 'year'
    params_get = { 'limit': 100 }
    baseUrl = f'/r/{subreddit}/{listing}?t={timeframe}'
    now = datetime.now()
    now_folder = datetime.today()
    redditImgDirectory = '/Users/aaroncarpenter/Desktop/Programming/Projects/bots/send_tweet_with_media_bot/reddit/images/'
    redditVideoDirectory = '/Users/aaroncarpenter/Desktop/Programming/Projects/bots/send_tweet_with_media_bot/reddit/videos/'
    image_directory_path = f'{redditImgDirectory}{subreddit}/{now_folder}'
    video_directory_path = f'{redditVideoDirectory}{subreddit}/{now_folder}'
    completedMedia = set()
    mediaAddedDict = {}
    # reddit_url = 'https://oauth.reddit.com/r/python/hot'
    
    def scrape_after_first_100(self, reddit_url, proxy_value, user_agent, after_keys_dict):
        """
        This method is responsible for scraping all subreddit pages after page 1.
        Input: The Request URL, A Proxy & User Agent To Hide Stop Potential Rate Limiting, And All Scraped After Keys
        
        
        
        """
        print('Additional Page Scraper Arguments/Input Values To Start', reddit_url, proxy_value, user_agent, after_keys_dict)
        l = 1
        currAfterKeyIdx = list(after_keys_dict)[0]
        try:
            while True or l < len(after_keys_dict) - 1:
                print(self.params_get)
                req = requests.get(reddit_url, headers=user_agent, params=self.params_get, proxies=proxy_value)
                res = req.json()
                posts = res['data']['children'] # where are the good data lives
                
                if len(posts) == 0:
                    print('No More Posts Found')
                    break
                
                print(f'L is moving brotha! {l}')
                post_titles = []
                after_key = res['data']['after']
                before_key = res['data']['before']
                currAfterKey = after_keys_dict[currAfterKeyIdx + 1] 
                self.params_get = { 'limit': 100, 'after': currAfterKey }
                listOfImageFiles = os.listdir(self.redditImgDirectory)
                post_image_urls = posts
                pulledPostImageUrls = []
                print(f'which page {l}, which key {currAfterKey} len of pull images {pulledPostImageUrls}')
                completedMedia = set()
                postData = {}
                postVideoURL = 'v.redd.it'
                postImageURL = 'i.redd.it'
                galleryURL = 'gallery'
                
                # while l < len(after_keys_dict) - 1:
                for j in range(len(posts) - 1):
                    postTitle =  posts[j]['data']['title']
                    post_image_url = posts[j]['data']['url_overridden_by_dest']
                    if postVideoURL in post_image_url:
                        postImage = post_image_urls[j]['data']['secure_media']['reddit_video']['fallback_url']
                    elif postImageURL in post_image_url:
                        postImage = post_image_urls[j]['data']['url_overridden_by_dest']
                    elif galleryURL in post_image_url:
                        continue;
                        
                    # Appending ALl Media URL's to the list to allows us
                    # the ability to loop through each value
                    if postImage not in completedMedia:
                        pulledPostImageUrls.append(postImage)
                        postData[postTitle] = [postImage, self.now]
                        
                # Loop over each media url that we have available in the request. 
                # We create a directory for the media to finally write the file to.
                mediaCounter = len(listOfImageFiles) + 1
                reqPicContent = []
                reqPicFileName = []
                for k in range(0, len(pulledPostImageUrls)):
                    currentMedia = pulledPostImageUrls[k]
                    
                    # Ensuring we have actual media on this post before continuing
                    if currentMedia != None:
                        mediaDictCount = len(self.mediaAddedDict)
                        self.mediaAddedDict[mediaDictCount + 1] = [self.now, currentMedia]
                        
                        if postVideoURL in currentMedia:
                            postMediaType = 'mp4'
                            fileBeingSaved = f'{self.video_directory_path}/reddit_Video_{self.subreddit}_{mediaCounter}page_{l}.{postMediaType}'
                            fileName = f'reddit_Video_{self.subreddit}_{mediaCounter}.{postMediaType}'
                            reqPicFileName.append(fileName)
                        elif postImageURL in currentMedia or galleryURL in currentMedia:
                            postMediaType = 'jpg'
                            fileBeingSaved = f'{self.image_directory_path}/reddit_Image_{self.subreddit}_{mediaCounter}page_{l}.{postMediaType}'
                            fileName = f'reddit_Image_{self.subreddit}_{mediaCounter}.{postMediaType}'
                            reqPicFileName.append(fileName)
                        
                        reqPicData = requests.get(currentMedia).content
                        reqPicContent.append(fileBeingSaved)
                        
                        # Create the folder for the image
                        if 'jpg' in currentMedia:
                            try:
                                if not os.path.exists(self.image_directory_path):
                                    os.makedirs(self.image_directory_path)
                            except Exception as e:
                                print(f'There was an error making the current media jpg file a directory {e}')
                        else:
                            try:
                                if not os.path.exists(self.video_directory_path):
                                    os.makedirs(self.video_directory_path)
                            except Exception as e:
                                print(f'There was an error making current media non-jpg file a directory {e}')
                        
                        # Write The Media to The Directory
                        with open(os.path.join(self.image_directory_path, fileBeingSaved), 'wb') as f:
                            f.write(reqPicData)
                            
                        with open(os.path.join(self.video_directory_path, fileBeingSaved), 'wb') as f:
                            f.write(reqPicData)
                            
                        mediaCounter += 1
                        print(f'Which file was saved? {fileBeingSaved} {self.params_get}')
                                        
                l += 1
                currAfterKeyIdx += 1            
            # directoryCounter += 1
        except Exception as e:
            print(f'An error Occurred In The Request Function! --> {e} Line Number: {str(traceback.extract_stack()[-1][1])}')
                
        