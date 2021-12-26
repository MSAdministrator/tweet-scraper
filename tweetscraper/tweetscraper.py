import re
import tweepy


class TweetScraper:

    DEFANG_URL_FINDER = re.compile(r"(?:ftp|h(?:xx|tt)ps?)://\S+")
    DEFANG_DOMAIN_FINDER = re.compile(r"\s((?=\S+\[\.\])((?:[a-z0-9-]+)(?:\.|\[\.\]))+[a-z]{2,}\S+)")

    def __init__(self, consumer_key, consumer_secret, access_token_key, access_token_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token_key, access_token_secret)
        self.api = tweepy.API(auth)

    def retweeted(self, data):
        text = None
        try: 
            text = data['retweeted_status']['extended_tweet']['full_text']
        except: 
            # Try for extended text of an original tweet, if RT'd (REST API)
            try: 
                text = data['retweeted_status']['full_text']
            except:
                # Try for extended text of an original tweet (streamer)
                try: 
                    text = data['extended_tweet']['full_text']
                except:
                    # Try for extended text of an original tweet (REST API)
                    try: 
                        text = data['full_text']
                    except:
                        # Try for basic text of original tweet if RT'd 
                        try: 
                            text = data['retweeted_status']['text']
                        except:
                            # Try for basic text of an original tweet
                            try: 
                                text = data['text']
                            except: 
                                # Nothing left to check for
                                text = ''
        return text

    def _extract_urls(self, string):
        return_list = []
        result = self.DEFANG_URL_FINDER.finditer(string)
        if result:
            for m in result:
                return_list.append(m.group())
        
        result = self.DEFANG_DOMAIN_FINDER.finditer(string)
        if result:
            for m in result:
                return_list.append(m.group())

        return return_list

    def on_status(self, tweet):
        if hasattr(tweet, "retweeted_status"):  # Check if Retweet
            try:
                return tweet.retweeted_status.extended_tweet["full_text"]
            except AttributeError:
                return tweet.retweeted_status.full_text
        else:
            try:
                return tweet.extended_tweet["full_text"]
            except AttributeError:
                return tweet.full_text

    def get_user_tweets(self, screen_name, count=200, since_id=None, include_rts=True, tweet_mode='extended'):
        """Get's a specific users tweets from their timeline

        Args:
            screen_name (str): The screen name of the user to retrieve tweets from.
            count (int, optional): The number of results to return. Defaults to 100.
            since_id ([type], optional): An ID of a tweet to start your search since. Defaults to None.
            include_rts (bool, optional): Include Retweets or not. Defaults to True.
            tweet_mode (str, optional): Extended will get longe tweets contents. Typically just keep it as extended. Defaults to 'extended'.

        Returns:
            list: Returns a list of tweets and different properties of each tweet.
        """
        return_list = []
        pages = 1
        if count >= 200:
            pages = int(count / 200) + 1
        
        for page in tweepy.Cursor(
            self.api.user_timeline,
            screen_name=screen_name,
            count=count,
            since_id=None if not since_id else since_id,
            tweet_mode=tweet_mode,
            include_rts=include_rts).pages(pages):
            for tweet in page:
                return_dict = {
                    'id': tweet.id,
                    'text': self.on_status(tweet)
                }
                
                tag_list = []
                for tag in tweet.entities['hashtags']:
                    tag_list.append(tag['text'])
                return_dict.update({'tags': tag_list})
                
                url_list = []
                expanded_url_list = []
                if hasattr(tweet, 'retweeted_status'):
                    try:
                        for url in tweet.retweeted_status.entities['urls']:
                            return_dict['tweet_text'] = return_dict['text'].replace(url['url'], url['expanded_url'])
                            url_list.append(url['url'])
                            expanded_url_list.append(url['expanded_url'])
                    except:
                        pass
                else:
                    try:
                        for url in tweet.entities['urls']:
                            return_dict['tweet_text'] = return_dict['tweet_text'].replace(
                                url['url'], url['expanded_url'])
                            url_list.append(url['url'])
                            expanded_url_list.append(url['expanded_url'])
                    except:
                        pass
                source_location = None
                try:
                    source_location = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id_str}"
                except:
                    pass
                return_dict.update({
                    'source_location': source_location,
                    'urls': url_list,
                    'expanded_urls': expanded_url_list,
                    'extracted_urls': self._extract_urls(return_dict['tweet_text'])
                })
                return_list.append(return_dict)
        return return_list

    def query(self, query="#opendir OR #phishkit OR #phishingkit", count=100, since_id=None, until=None):
        """Queries Twitter based on the provided query

        Args:
            query (str, optional): The Twitter search query you want to search for. Defaults to "#opendir OR #phishkit OR #phishingkit".
            count (int, optional): The number of results to return. Defaults to 100.
            since_id ([type], optional): An ID of a tweet to start your search since. Defaults to None.
            until ([type], optional): Returns tweets created before the given date. Date should be formatted as YYYY-MM-DD. Keep in mind that the search index has a 7-day limit. In other words, no tweets will be found for a date older than one week. Defaults to None.

        Returns:
            list: Returns a list of tweets and different properties of each tweet.
        """
        return_list = []
        pages = 1
        if count >= 200:
            pages = int(count / 200) + 1
        for page in tweepy.Cursor(
            self.api.search_tweets,
            q=query,
            count=count,
            result_type="recent",
            include_entities=True,
            lang="en",
            since_id=None if not since_id else since_id,
            until=None if not until else until,
            tweet_mode="extended").pages(pages):
            for tweet in page:
                return_dict = {
                    'id': tweet.id,
                    'text': self.on_status(tweet)
                }
                
                tag_list = []
                for tag in tweet.entities['hashtags']:
                    tag_list.append(tag['text'])
                return_dict.update({'tags': tag_list})
                
                url_list = []
                expanded_url_list = []
                if hasattr(tweet, 'retweeted_status'):
                    try:
                        for url in tweet.retweeted_status.entities['urls']:
                            return_dict['tweet_text'] = return_dict['text'].replace(url['url'], url['expanded_url'])
                            url_list.append(url['url'])
                            expanded_url_list.append(url['expanded_url'])
                    except:
                        pass
                else:
                    try:
                        for url in tweet.entities['urls']:
                            return_dict['tweet_text'] = return_dict['tweet_text'].replace(
                                url['url'], url['expanded_url'])
                            url_list.append(url['url'])
                            expanded_url_list.append(url['expanded_url'])
                    except:
                        pass
                source_location = None
                try:
                    source_location = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id_str}"
                except:
                    pass
                return_dict.update({
                    'source_location': source_location,
                    'urls': url_list,
                    'expanded_urls': expanded_url_list,
                    'extracted_urls': self._extract_urls(return_dict['tweet_text']) if return_dict.get('tweet_text') else None
                })
                return_list.append(return_dict)
        return return_list
