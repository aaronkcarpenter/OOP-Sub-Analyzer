import remove_saved_media
import write_filenames_to_text_file


class AddMedia:
    media_cleaning_instance = remove_saved_media.MediaCleaning()
    write_to_file_instance = write_filenames_to_text_file.WriteFilesToCSV()
    # remove_media = media_cleaning_instance.removeSavedMedia()
    completedMedia = set()
    
    def addSavedMediaToCompleted(self, media_urls):
        """
        Add saved media to a set of completed content
        """
        try:
            for url in media_urls:
                if url != None:
                    self.completedMedia.add(url)
                    print(f'URL added to completed media set {url}')
            self.write_to_file_instance.writeFileNamesToTextFile()
            self.media_cleaning_instance.removeSavedMedia(media_urls)
        except Exception as e:
            print(f'There Was an error when adding the completed media to the set {e}.')
                
# if __name__ ==  "__main__":
#     media_saving_instance = AddMedia()
#     add_media = media_saving_instance.addSavedMediaToCompleted()