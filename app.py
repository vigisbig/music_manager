import os
import requests
import tweepy
from git import Repo

# Twitter API credentials
twitter_api_key = '3P3ZCSR0R7fOgIBp954wTz4sX'
twitter_api_secret = 'N6UHu4z8RFgBGXsd0QcXD5jiRor2Bu1Bd6tuPJ6JSbwfKBZ4Bl'
twitter_access_token = '84854703-Ucow9TlPRQmEWMv2QKDBZI90lZMIymtbiksndof8O'
twitter_access_token_secret = '7q9DpjgUlRfekJBkiwRAJVoOthnloNuPZSfCnVu2JkQ53'

# Twitter API v2 Bearer Token
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAO7EnQEAAAAACsOG0QE74tQsqBvFM6YFWIYP8Q8%3DyFPPIJ9cz4JqweUOTiJXo3145sN7OQNV9aTgUailGFX0NrJl8j'

# Git repository information
git_repo_path = '/path/to/your/git/repo'
git_repo_url = 'https://github.com/vigisbig/music_manager.git'

# Function to extract YouTube links from tweets
def extract_youtube_links(tweet):
    urls = []
    for url in tweet['entities']['urls']:
        expanded_url = url['expanded_url']
        if 'youtube.com' in expanded_url or 'youtu.be' in expanded_url:
            urls.append(expanded_url)
    return urls

# Function to update Git repository
def update_git_repo(file_path, data):
    repo = Repo(git_repo_path)
    
    # Pull latest changes
    repo.remotes.origin.pull()

    # Check for uniqueness and append to file
    with open(file_path, 'a') as file:
        for link in data:
            if link not in repo.git.show('HEAD:' + file_path):
                file.write(f"{link}\n")

    # Commit and push changes
    repo.index.add([file_path])
    repo.index.commit("Update YouTube links")
    repo.remotes.origin.push()

# Main function
def main():
    # Authenticate with Twitter API v2
    auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret)
    auth.set_access_token(twitter_access_token, twitter_access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Fetch tweets with the #music hashtag using Twitter API directly
    url = "https://api.twitter.com/2/tweets"
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    params = {
        "tweet.fields": "entities",
        "user.fields": "username",
        "expansions": "author_id"
    }
    response = requests.get(url, headers=headers, params=params)
    tweets = response.json()['data']

    # Extract YouTube links from relevant tweets
    youtube_links = []
    for tweet in tweets:
        if tweet['text'].endswith('#music'):
            youtube_links.extend(extract_youtube_links(tweet))

    # Update Git repository with unique links
    if youtube_links:
        git_file_path = 'youtube_links.md'
        update_git_repo(git_file_path, youtube_links)
        print("YouTube links updated successfully.")
    else:
        print("No relevant tweets found.")

if __name__ == "__main__":
    main()
