import tweepy
import boto3

class CreateTweetsWithMedia:
    """
    
    """
    
    def __init__(self, tweet_text: str, media_id: int, counter: int) -> None:
        self.tweet_text = tweet_text
        self.media_id = media_id
        self.counter = counter
        
    def lambda_handler(self, event, context):
        self.create_media_tweet()
        
    def get_twitter_keys_from_aws_secrets(self) -> dict:
        """
        This function pulls the auth Tokens and Keys from AWS Systems Manager
        parameter store, which is needed for the bot to access Twitter.
        Retrieve secrets from Parameter Store.
        
        We connect to  aws via our boto package and once we have access,
        we take the needed k/v's from the store. To make access to the values
        simple, we store each of the keys in a dictionary that we ultimately
        pass to our Twitter client when attempting to create an automated tweet.
        """
        aws_client = boto3.client('ssm')
        parameters = aws_client.get_parameters(
            Names=[
                'bearer_token',
                'consumer_key',
                'consumer_secret',
                'access_token',
                'token_secret'
            ],
            WithDecryption=True
        )

        keys = {}
        for parameter in parameters['Parameters']:
            keys[parameter['Name']] = parameter['Value']
        return keys
    
    def connect_twitter_client(self) -> None:
        """
        This function is used to connect the bot to the correct
        Twitter account after getting the proper credentials
        from the AWS Parameter Store.
        
        Once authorized, the bot is ready to tweet.
        """
        auth_creds = self.get_twitter_keys_from_aws_secrets()
        client = tweepy.Client(
                        bearer_token=auth_creds['bearer_token'], #1
                        consumer_key=auth_creds['consumer_key'], #2
                        consumer_secret=auth_creds['consumer_secret'], #4
                        access_token=auth_creds['access_token'], #0
                        access_token_secret=auth_creds['token_secret'],
                        wait_on_rate_limit=True
            )
    
        return client

    def create_media_tweet(self) -> None:
        client = self.connect_twitter_client()
        try:
            tweet_num = 1
            media_tweet = client.media_upload(self.media_id)
            tweet = 'Twitter Classic #{tweet_num}'
            update_status = client.update_status(status=tweet, media_ids=[media_tweet.media_id])
            print('Tweet with Image Successfully Sent')
        except:
            print('Problem Sending The Tweet')
            
    def check_for_rate_limiting(self) -> None:
        """
        Check how many Tweets have been made and compare it
        against the total that are accepted 15/60/24 hrs.
        """
        pass
            
def main() -> None:
    """
    This is where the useful work the script does is filtered. For example, this function
    is where I would  call create_media_tweet.
    """
    media_status_update = CreateTweetsWithMedia.create_media_tweet()
    run_via_aws_lambda = CreateTweetsWithMedia.lambda_handler()
    
        
if __name__ == "__main__":
    main()
    
"""
Potential Lifecycle of this Class:
- Initial: Get the credentials needed to make a new tweet. We will need to
connect to AWS first, to obtain the Twitter Credentials from the systems manager.

- Middle: Once credentials are approved and received, we now need to pull the media
as well as string for the status from somewhere. Currently, that will be either the S3
bucket for the image, and Google Sheets for the status to go with it.

- End: Once the tweet has all necessary parts: auth, media, tweet, we can send the
status out, leaving the object with nothing more to do.

"""