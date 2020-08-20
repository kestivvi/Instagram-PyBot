# Instagram PyBot
Instagram PyBot is my project to learn how to build web browser bots with Python and Selenium. 

## Installation
Requirements:
* Chrome/Chromium browser
* chrome webdriver
* Python 3.8.0+
* module selenium
* module pandas

Those Python modules are in requirements.txt

After downloading repository, in top level folder run:
```bash
pip install -r requirements.txt
```

Download appropriate version of chromedriver for your Chrome/chromium browser and operating system
https://chromedriver.chromium.org/downloads

Then unpack chromedriver.exe and put somewhere, that you know where it's at ;)

## Getting started
Firstly init your new bot with this command
```bash
python main.py init <dirpath>
```
where dirpath is the directory where setting and other data about the bot will be stored.


Then configure a bot settings, to do so enter directory you specified earlier. There are a couple of files you'll be interested to configure.

* config.json - There are settings about program and bot behaviour.
    * **web_browser_driver - You have to specify path to your chromedriver you have downloaded before.** 
    * headless - If true, browser will be opened in background and it won't be rendered on the screen.
    * verbose - If true, gives nice live dashboard with some stats.
    * checking_frequency - Time in seconds between bot sessions, from bot logging out to bot logging in.
    * chances - Bot browsing posts have a chance to do specific things.
    * unfollow_non_followers_first - If true, while unfollowing people at the end of every session bot will be unfollowing people that doesn't follow you in the first place, then people that follow you.
    * min_of_followings - The lowest number of people you follow
    * max_of_followings - The highest number of people you follow
    * maxes per day - The highest number of given action the bot can do in 24 hours.
    * maxes per hour - The highest number of given action the bot can do in 1 hour.
* **secret.txt - Your login and password to instagram account should be there. First line login (name or email), second line password.**
* comments.txt - Each line is a template comment that the bot will be using.
* emojis.txt - Each line is a emoji that the bot can use. When commenting the bot may use from 0 to 3 different emojis at the very end of comment.
* sites.txt - Each line is a instagram site where bot will be working. Site can be a hashtag like "#cat" or person like "taylorswift"
* following_whitelist.txt - The bot has a chance to unfollow, but it won't unfollow people which are on this whitelist. On each line should be separate name
* likelist.txt - When the bot logged in, it will enter these sites (hashtags or people) to check 3 first posts and like them.

Then you can run:
```bash
python main.py start <dirpath>
```
where dirpath is the directory you have initiated the bot settings.

## License
[MIT](https://choosealicense.com/licenses/mit/)
