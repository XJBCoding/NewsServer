# News Server

This app is a news aggregator that provides users with ability to find popular news and search by keyworkds and sources. Users also are able see personal analytics based on the articles they have clicked.

## Build
This Flask app does not require a build. It can just be run.

## Install
To install required Python packages:
```
pip install -r requirements/dev.txt
```

## Operate
To run:
```
python news_server.py
```

### Login
Upon first starting the app, users will be able to register for a new account or sign into an existing account.

### Homepage 
After logging in, the user will be directed to the homepage with various features.

#### Trending topics
Here, they will see blue text for trending topics, according to the Google News API.

#### Articles
They will also be able to see cards representing various popular articles for the day, retrieved by the News API. Each card shows:
* an image
* the headline
* the estimated reading time (assuming a reading speed of 200 words-per-minute)
* a topic (produced by a Naive Bayes classifier trained on old news articles)

#### Search by Keywords & Source
The user also has access to search functionality. They can search by any combination of keywords or IDs of news organizations (e.g. `abc-news`, `cnn`)

### Personalized User Analytics
On the analytics page, the user can view statistics based on a history of what they have read. This includes:
* time analytics (how many minutes a user has read each day)
* topic analytics (what topics a user has read)

## Test
For pre-commit testing, set it up like so:
```
./bin/git-hooks/hook-setup.sh
```

In order to correctly push logs, we have to make a local branch `logs`
```
git checkout -b logs
git branch -u origin/logs
```

The process for commiting is as follows:
```
git checkout master
# Develop on master branch
git commit                  # The pre-commit will run

git checkout logs
git add logs
git commit
git push                    # This will push to the remote branch origin/logs

git checkout master
git push                    # This will push to the remote branch origin/master
```

For post-commit CI, we use [Travis](https://travis-ci.com/XJBCoding/NewsServer).

