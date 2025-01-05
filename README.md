Preview
========================
![image](https://i.imgur.com/eWhPKHD.png)


Getting your Headers
========================

1. Go to your twitter profile (or the user you want to monitor)
2. Open up your inspect element and click on your network tab
3. You'll most likely need to refresh the tab
4. search for "tweets"
5. Right click, go down to copy, and click Copy as cURL (example below)
![Screenshot 2024-04-30 215312](https://i.imgur.com/VgKjfnH.png)

Copying your Headers
========================
1. Go here: https://curlconverter.com/ and paste the copied cURL into the top box, this will display your headers 
2. Copy the url at the bottom and paste that into "url = "PASTE HERE"
3. Paste your cookies, headers, and params into the code

Filling out webhook info
========================
1. Open webhooks.txt
2. Paste in your webhook url
3. save the file
4. RUN THE SCRIPT

Other info
========================
This will automatically make a file named "sent_tweet_ids.txt". this will be used so it doesn't send duplicate tweets
This script will ONLY send the newest tweets even when it first starts
This script most likely will get rate limited so be aware :)

[!["Support the project!"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://cash.app/$WRDSY)
