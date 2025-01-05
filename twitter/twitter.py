import requests
import time
import json
import os
import re

with open("webhooks.txt", "r") as file:
    DISCORD_WEBHOOK_URLS = [line.strip() for line in file.readlines()]

# REPLACE THIS WITH THE URL YOU GET FROM YOUR CURL
url = ""

cookies = {

}

headers = {

}

params = {

}

def read_sent_tweet_ids():
    if os.path.exists("sent_tweet_ids.txt"):
        with open("sent_tweet_ids.txt", "r") as file:
            return set(line.strip() for line in file.readlines())
    return set()


def save_sent_tweet_id(tweet_id):
    with open("sent_tweet_ids.txt", "a") as file:
        file.write(f"{tweet_id}\n")

sent_tweet_ids = read_sent_tweet_ids()
last_checked_tweet_id = max(map(int, sent_tweet_ids), default=None)

def send_discord_message(content, image_url=None):
    for webhook_url in DISCORD_WEBHOOK_URLS:
        data = {
            "embeds": [{
                "description": content,
                "color": 0x27a9ff,
                "image": {"url": image_url} if image_url else None,
                "footer": {
                    "text": "Savings Squad Deals",
                    "icon_url": "https://pbs.twimg.com/profile_images/1708899711283793920/yHqgXwrv_400x400.jpg"
                }
            }]
        }
        requests.post(webhook_url, json=data)

def extract_first_link(tweet_text):
    urls = re.findall(r'(https?://\S+)', tweet_text)
    if urls:
        first_url = urls[0] 
        tweet_text = tweet_text.replace(urls[-1], '').strip()
    else:
        first_url = None
    
    return tweet_text, first_url

def check_for_new_tweets():
    global last_checked_tweet_id
    response = requests.get(url, params=params, cookies=cookies, headers=headers)

    if response.status_code == 200:
        instructions = response.json().get('data', {}).get('user', {}).get('result', {}).get('timeline_v2', {}).get('timeline', {}).get('instructions', [])
        
        new_tweet_ids = []

        for instruction in instructions:
            if 'entries' in instruction:
                for entry in instruction['entries']:
                    if entry['entryId'].startswith('tweet-'):
                        tweet = entry['content']['itemContent']['tweet_results']['result']
                        tweet_id = tweet['rest_id']
                        tweet_text = tweet['legacy']['full_text']

                        if last_checked_tweet_id is None or int(tweet_id) > last_checked_tweet_id:
                            cleaned_text, first_url = extract_first_link(tweet_text)
                            image_url = tweet['legacy'].get('extended_entities', {}).get('media', [{}])[0].get('media_url_https')

                            send_discord_message(cleaned_text, image_url)

                            save_sent_tweet_id(tweet_id)
                            new_tweet_ids.append(int(tweet_id))

        if new_tweet_ids:
            last_checked_tweet_id = max(new_tweet_ids)

    else:
        print(f"Failed to retrieve tweets. Status code: {response.status_code}")

while True:
    check_for_new_tweets()
    time.sleep(60)
