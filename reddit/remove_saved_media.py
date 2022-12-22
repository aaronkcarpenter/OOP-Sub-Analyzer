    
class MediaCleaning:
    
    def removeSavedMedia(self, mediaList):
        """
        Remove All Scraped Url's from the media list after they've been added to the completedMedia set
        """
        try:
            mediaList.clear()
        except Exception as e:
            print(f'There Was an error when removing the urls from the list {e}.')
                
if __name__ ==  "__main__":
    media_cleaning_instance = MediaCleaning()
    remove_media = media_cleaning_instance.removeSavedMedia()