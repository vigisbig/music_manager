import tweepy
import re
from git import Repo

# Replace these with your own Twitter API credentials
bearer_token = "AAAAAAAAAAAAAAAAAAAAAO7EnQEAAAAA5eazEhkX%2FQCV%2BKlOFFS%2B4i2V8Ss%3DDknHnOiD9L8L2Pmgp5EtRL6MOuiIQ78n6iQpqQNkJcALFfkuGR"
client = tweepy.Client(bearer_token=bearer_token)

# Git repository information (assuming you already have a markdown file)
repo_path = "D:\Fintools\music_manager"
file_name = "Music.md"

def find_music_links(tweets):
  """
  Finds unique YouTube links from tweets ending with #music hashtag.

  Args:
    tweets: A list of tweet objects.

  Returns:
    A set of unique YouTube links.
  """
  links = set()
  for tweet in tweets:
    text = tweet.text.lower()
    if text.endswith("#music"):
      # Extract Youtube link using regular expression
      match = re.search(r"https?://(?:www\.)?youtu(?:\.be|be\.com)/(.+)$", text)
      if match:
        link = f"[Watch this music video!]({match.group(1)})"
        links.add(link)
  return links

def update_markdown_file(links):
  """
  Appends unique YouTube links to a markdown file in a git repository.

  Args:
    links: A set of unique YouTube links.
  """
  with open(f"{repo_path}/{file_name}", "a+") as f:
    for link in links:
      f.write(f"\n* {link}")
    f.flush()

  # Commit changes to git repository
  repo = Repo(repo_path)
  repo.index.add(file_name)
  repo.index.commit(f"Adding new music links from tweets")
  origin = repo.remote("origin")
  origin.push()

def main():
  # Get last 50 tweets from your account
  tweets = client.get_user_tweets(client.me().id, max_results=50)

  # Find unique YouTube links from music tweets
  unique_links = find_music_links(tweets)

  # Update markdown file only if there are unique links
  if unique_links:
    update_markdown_file(unique_links)
    print(f"Successfully added {len(unique_links)} unique music links to {file_name}")
  else:
    print("No new music links found in your tweets.")

if __name__ == "__main__":
  main()
