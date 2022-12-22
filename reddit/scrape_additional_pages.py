import get_user_agent
import pull_proxy_list
import auth_reddit
import remove_saved_media
import add_saved_media
import write_filenames_to_text_file
import get_keys_to_scrape
import os
import requests
import traceback
from datetime import datetime

class AdditionalPageScraper:

    # reddit_authentication_obj = auth_reddit.AuthenticateRedditBot()
    # reddit_authentication_url = reddit_authentication_obj.getRedditAuth()
    # proxy_value_obj = pull_proxy_list.PullFreshProxyList()
    # proxy_value = proxy_value_obj.proxySteps()
    # user_agent_object = get_user_agent.GetUserAgent()
    # new_user_agent = user_agent_object.random_user_agent()
    # remove_saved_media_obj = remove_saved_media.MediaCleaning()
    # remove_media  = remove_saved_media_obj.removeSavedMedia()
    # media_saving_instance = add_saved_media.AddMedia()
    # add_media = media_saving_instance.addSavedMediaToCompleted()
    # get_after_keys_obj = get_keys_to_scrape.PullAllAfterKeys()
    # after_key_dict = get_after_keys_obj.getAllAfterKeys()
    # filename_to_csv_instance = write_filenames_to_text_file.WriteFilesToCSV()
    # write_to_csv = filename_to_csv_instance.writeFileNamesToTextFile()
    
    subreddit = 'BlackPeopleTwitter'
    limit = 100
    timeframe = 'all'
    listing = 'year'
    params_get = { 'limit': 100 }
    baseUrl = f'/r/{subreddit}/{listing}?t={timeframe}'
    redditImgDirectory = '/Users/aaroncarpenter/Desktop/Programming/Projects/bots/send_tweet_with_media_bot/reddit/images/'
    redditVideoDirectory = '/Users/aaroncarpenter/Desktop/Programming/Projects/bots/send_tweet_with_media_bot/reddit/videos/'
    completedMedia = set()
    now = datetime.now()
    mediaAddedDict = {}
    
    def scrapeAdditionalPages(self, reddit_authentication_url, proxy_value, after_key_dict, user_agent):
        """_scrapeAdditionalPages_
            After we've scraped the after keys, we have the needed data to scrape all pages available
            after page 1.
        """
        try:    
            l = 1
            currAfterKeyIdx = list(after_key_dict)[0]
            
            print(len(list(os.walk('/reddit/postImage/'))))
            totalFolders = len(list(os.walk('/reddit/postImage/')))
            directoryCounter = totalFolders + 1
            dirName = f'{self.redditImgDirectory}/{directoryCounter}/'
                
            while l < len(after_key_dict) - 1:
                currAfterKey = after_key_dict[currAfterKeyIdx]
                params_get = { 'limit': 100, 'after': currAfterKey }
                req = requests.get(reddit_authentication_url, headers=user_agent, params=self.params_get, proxies=proxy_value)
                res = req.json()
                posts = res['data']['children']            
                listOfImageFiles = os.listdir(self.redditImgDirectory)
                post_image_urls = posts
                pulledPostImageUrls = []
                print(f'which page {l}, which key {currAfterKey} len of pull images {pulledPostImageUrls}')
                completedMedia = set()
                postData = {}
                postVideoURL = 'v.redd.it'
                postImageURL = 'i.redd.it'
                galleryURL = 'gallery'
                
                
                for j in range(0, len(posts) - 1):
                    postTitle =  posts[j]['data']['title']
                    post_image_url = posts[j]['data']['url_overridden_by_dest']
                    if postVideoURL in post_image_url:
                        postImage = post_image_urls[j]['data']['secure_media']['reddit_video']['fallback_url']
                    elif postImageURL in post_image_url:
                        postImage = post_image_urls[j]['data']['url_overridden_by_dest']
                    elif galleryURL in post_image_url:
                        continue;
                        
                    # lastPeriod = postImage.rfind('.')
                    # postMediaType = postImage[lastPeriod + 1:]
                    if postImage not in completedMedia:
                        pulledPostImageUrls.append(postImage)
                        postData[postTitle] = [postImage, self.now]
                        
                # mediaCounter = len(listOfImageFiles) + 1
                mediaCounter = 1
                reqPicContent = []
                reqPicFileName = []
                
                """Create target Directory if don't exist"""
                if not os.path.exists(dirName):
                    os.mkdir(dirName)
                    print("Directory " , dirName ,  " Created ")
                else:    
                    print("Directory " , dirName ,  " already exists")
                    
                for k in range(0, len(pulledPostImageUrls) - 1):
                    currentMedia = pulledPostImageUrls[k]
                    mediaDictCount = len(self.mediaAddedDict)
                    self.mediaAddedDict[mediaDictCount + 1] = [self.now, currentMedia]
                    if postVideoURL in currentMedia:
                        postMediaType = 'mp4'
                        fileBeingSaved = f'{self.redditVideoDirectory}/{directoryCounter}/reddit_Video_{self.subreddit}_{mediaCounter}.{postMediaType}'
                    elif postImageURL in currentMedia or galleryURL in currentMedia:
                        postMediaType = 'jpg'
                        fileBeingSaved = f'{self.redditImgDirectory}/{directoryCounter}/reddit_Media_{self.subreddit}_{mediaCounter}.{postMediaType}'
                        
                    reqPicData = requests.get(currentMedia).content
                    reqPicContent.append(fileBeingSaved)
                
                    savePath = dirName
                    fileName = fileBeingSaved
                    completeName = os.path.join(savePath, fileName)
                    with open(f'{fileBeingSaved}', 'wb') as f:
                        f.write(reqPicData)
                    
                    mediaCounter += 1
                    print(f'Which file was saved? {fileBeingSaved}')
                # awsConnection.uploadToS3(reqPicContent, reqPicFileName) # uncomment when i have it worked out to avoid s3 charges
                
                if l == list(self.after_key_dict)[-1]:
                    self.add_media(pulledPostImageUrls)
                                            
                if l == 3:
                    print('3 Pages Scraped, Ending Now')
                    self.write_to_csv()
                    break
                
                l += 1
                currAfterKeyIdx += 1            
                directoryCounter += 1
                dirName = f'{self.redditImgDirectory}/{directoryCounter}/'
                
        except Exception as e:
            print(f'An error Occurred In The Additional Pages To Scrape Function! --> {e} Line Number: {str(traceback.extract_stack()[-1][1])}')
            
if __name__ == "__main__":
    additional_page_scraper_obj = AdditionalPageScraper()
    run_additional_page_scraper = additional_page_scraper_obj.scrapeAdditionalPages()