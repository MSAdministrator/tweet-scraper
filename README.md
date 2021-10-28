# tweet_scraper

Used to search twitter by query or a specific users Twitter timeline.

## Getting Started

To use `twitter-scraper` to search Twitter you will need to have a Twitter account, but you will also need to generate some keys to post to twitter. To do this, you will need to create a Twitter Application.

The first step is to visit https://dev.twitter.com/apps/new and create a new Twitter application. When you create a new Twitter application you will need to provide the required information.

Next, you will need to select the “Keys and Tokens” tab and gather all your keys. Please keep these secure! We will be using them to authenticate to Twitter's API.

At the end you should have 4 keys:

* consumer_key
* consumer_secret
* access_token_key
* access_token_secret


### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
python setup.py install
```

## Usage

You will use this project either via the command line or a Python package.

### Command Line

```
twitter-scraper --consumer_key {some value} --consumer_secret {some value} --access_token_key {some value} --access_token_secret {some value} get_user_tweets --screen_name 'MSAdministrator'

twitter-scraper --consumer_key {some value} --consumer_secret {some value} --access_token_key {some value} --access_token_secret {some value} query
```

### Package

```python
from twitter_scraper import TwitterScraper

ts = TwitterScraper(
    consumer_key={some value},
    consumer_secret={some value},
    access_token_key={some value},
    access_token_secret={some value}
)

for item in ts.get_user_tweets('MSAdministrator'):
    print(item)

```

## Built With

* [carcass](https://github.com/MSAdministrator/carcass) - Python packaging template

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. 

## Authors

* Josh Rickard - *Initial work* - [MSAdministrator](https://github.com/MSAdministrator)

See also the list of [contributors](https://github.com/MSAdministrator/tweet-scraper/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details
