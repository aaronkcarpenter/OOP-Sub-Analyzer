import tweepy
import boto3

def lambda_handler(event, context):
    """Lambda function That automates tweet sending of a twitter bot."""
    create_media_tweet()

def getClientAWS():
    """
    This function is used to connect the bot to the correct
    Twitter account after getting the proper credentials
    from the AWS Parameter Store.
    
    Once authorized, the bot is ready to tweet.
    """
    auth_creds = get_twitter_keys()
    client = tweepy.Client(
                        bearer_token=auth_creds['bearer_token'], #1
                        consumer_key=auth_creds['consumer_key'], #2
                        consumer_secret=auth_creds['consumer_secret'], #4
                        access_token=auth_creds['access_token'], #0
                        access_token_secret=auth_creds['token_secret'],
                        wait_on_rate_limit=True
            )
    return client

def get_twitter_keys():
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
    
def create_media_tweet():
    client = getClientAWS()
    try:
        # Tweet a new tweet
        # tweet = 'After my first Muay Thai training session I said fuck it and just went and got a glock.'
        media_tweet = client.media_upload('popeyes_biscuit.jpg')
        tweet = 'Yall a nigga was ALMOST on a shirt. Just had a @popeyes biscuit.'
        update_status = client.update_status(status=tweet, media_ids=[media_tweet.media_id])
        print('Tweet with Image Successfully Sent')
    except:
        print('Problem Sending The Tweet')
        

