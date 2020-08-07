# Instagram PyBot
Instagram PyBot is my project to learn how to build web browser bots with Python and Selenium. 

## Installation
Requirements:
* Chrome/Chromium
* chrome webdriver
* Python
* module selenium
* module pandas

Those Python modules are in requirements.txt

After downloading repository, in top level folder run:
```bash
pip install -r requirements.txt
```

## Getting started
In "sample" folder is one example of files that are mandatory for bot to run correctly

Settings for the bot you can provide via cmd line arguments or config.json file. Cmd line arguments have the highest piority.

In the config.json is configuration of bot. **You have to provide path to your chrome webdriver!**

You can choose files the bot will use, like file with credential for login **(secret.txt is empty, you have to provide your credentials)**, sites where bot will be liking, sample comments and emojis to them. You can also set the behaviour of the bot, what is the limit of likes per hour, per day and so on.

**In file with credentials, in the first line should be login (username or email) and in the second line password.** 

In file with sites, they should be listed each in new line. Bot will be randomly choosing one when it's gonna change site. Names with a "#" at the very beginning lead to hashtag sites. Names without a "#" at the very beginning lead to profile sites.

In file with comments, they should be listed each in new line. Bot will be randomly choosing one when it's gonna comment.

In file with emojis, they should be listed each one (exactly one) in new line. Bot will be randomly choosing one when it's gonna add from 0 to max 3 emojis after comment.

Then you can run:
```bash
python main.py
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
