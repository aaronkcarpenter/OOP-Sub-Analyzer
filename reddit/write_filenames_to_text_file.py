import os

class WriteFilesToCSV:
    fileName = './media_saved_names.txt'
    redditImgDirectory = '/Users/aaroncarpenter/Desktop/Programming/Projects/bots/send_tweet_with_media_bot/reddit/images/'
    redditVideoDirectory = '/Users/aaroncarpenter/Desktop/Programming/Projects/bots/send_tweet_with_media_bot/reddit/videos/'
    
    def is_file_empty(self):
        return os.path.isfile(self.fileName) and os.path.getsize(self.fileName) == 0
            
    def writeFileNamesToTextFile(self):
        file_list = []
        is_txt_empty = self.is_file_empty()
        try:
            if is_txt_empty:
                fileCounter = 1
                print('in the if')
                with open(self.fileName, 'w') as f:
                    for file in os.listdir(self.redditImgDirectory):
                        print(f'FileName is: {file}')
                        f.write(f'{fileCounter}.{file}' + '\n')
                        # f.write('\n')
                        fileCounter += 1
                        
                    for file in os.listdir(self.redditVideoDirectory):
                        print(f'FileName is: {file}')
                        f.write(''.join(file) + '\n')
                        # f.write('\n')
                        fileCounter += 1
            else:
                print('in the else meaning the file is NOT empty')
                with open(f'{self.fileName}', 'r', encoding= 'utf-8') as f:
                    # Get the next available empty line to write on via Readlines
                    fileCounter = len(f.readlines()) + 1
                
                # with open(self.fileName, 'a') as f:
                for file in os.listdir(self.redditImgDirectory):
                    file_list.append(file)
                    # f.write(f'ac {file} \n')
                    # f.write(''.join(file) + '\n')
                    # print(f'FileName isssssss: {file}')
                    # f.write('\n')
                    fileCounter += 1
                    
                with open(f'{self.fileName}', 'a') as f:
                    for file in file_list:
                        f.write(f'ac {file} \n')
                        
                for file in os.listdir(self.redditVideoDirectory):
                    f.write(''.join(file) + '\n')
                    print(f'FileName is: {file}')
                    # f.write('\n')
                    fileCounter += 1 
                        
            f.close()
        except Exception as e:
            print(f'An error occurred while writing to text file {e}')
            
if __name__ == "__main__":
    filename_to_csv_instance = WriteFilesToCSV()
    write_to_csv = filename_to_csv_instance.writeFileNamesToTextFile()