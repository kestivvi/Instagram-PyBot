import argparse, json, sys
from path import Path

class _CONFIG_DEFAULT:
    ################################
    # If there is no "config.json" file, these will be default settings.
    # Json file takes piority over this class

    credential_file = "./sample/secret.txt"
    login = ""
    password = ""

    comments_file = "./sample/comments.txt"
    emojis_file = "./sample/emojis.txt"
    sites_file = "./sample/sites.txt"

    json_config = "./sample/config.json"
    statistics_folder = "./sample/statistics/"
    # web_browser = ""
    web_browser_driver = ""
    headless = False

    verbose = False
    checking_frequency = 30*60

    chance_of_change_site = 1/30
    chance_of_like = 0.8
    chance_of_comment = 0.1
    chance_of_follow = 0.4
    chance_of_unfollow = 1/50

    min_of_followings = 100
    max_of_followings = 120

    max_likes_per_hour = 35
    max_comments_per_hour = 5
    max_follows_per_hour = 7
    max_unfollows_per_hour = 7

    max_likes_per_day = 300
    max_comments_per_day = 20
    max_follows_per_day = 100
    max_unfollows_per_day = 100


data = _CONFIG_DEFAULT()


def make_enum(name, values):
    _k = _v = None
    class TheEnum():
        nonlocal _k, _v
        for _k, _v in values.items():
            locals()[_k] = _v
    TheEnum.__name__ = name
    return TheEnum


def check_json_config():
    if Path(data.json_config).exists():
        with open(Path(data.json_config)) as f:
            return make_enum("data",json.load(f))
    elif not Path(_CONFIG_DEFAULT.json_config).exists():
        print('[WARNING]: Default json config file is not exist.')
    else:
        print('[WARNING]: Specified json config file is not exist.')
        return _CONFIG_DEFAULT


def handle_args():
        
    config_default = _CONFIG_DEFAULT
    
    parser = argparse.ArgumentParser(prog="Instagram PyBot",
                                     usage='%(prog)s [options]',
                                     description="""Instagram Bot written in Python and Selenium.
                                                    It can like, comment, follow and unfollow.""")
    parser.version = '0.1.0'
    

    try: json_config_index = sys.argv.index("-jc")
    except ValueError:
        json_config_index = None
    
    if json_config_index == None:
        try: json_config_index = sys.argv.index("--json_config")
        except ValueError:
            pass
    
    if json_config_index != None:
        config_default.json_config = sys.argv[json_config_index+1]
        
    config_default = check_json_config()
    
    ################################
    # Credentials

    parser.add_argument('-cf', '--credential_file',
                        help="""File with credentials to login.
                        First line should be email or username, second line should be password""",
                        default=config_default.credential_file,
                        type=str)
    
    parser.add_argument('-l', '--login',
                        help="Email or username to login.",
                        default=config_default.login,
                        type=str)
    
    parser.add_argument('-p', '--password',
                        help="Password to login.",
                        default=config_default.password,
                        type=str)

    
    ################################
    # Sample Files

    parser.add_argument('-c', '--comments_file',
                        help="File with comments sample.",
                        default=config_default.comments_file,
                        type=str)

    parser.add_argument('-e', '--emojis_file',
                        help="File with emojis sample.",
                        default=config_default.emojis_file,
                        type=str)

    parser.add_argument('-s', '--sites_file',
                        help="File with sites (hashtags or people) where bot should like, comment and follow.",
                        default=config_default.sites_file,
                        type=str)
    

    ################################
    # Other Files

    parser.add_argument('-jc', '--json_config',
                        help="""Path to json file with config.
                                It can be updated while program is working.
                                Command line arguments have the highest piority,
                                then is json file and at the end default spiecified in _CONFIG_DEFAULT class in config.py""",
                        default=config_default.json_config,
                        type=str)

    parser.add_argument('-st', '--statistics_folder',
                        help="""Folder where bot can save statistics data about likes, comments, follows, unfollows and errors.
                                These are mandatory to bot works corectly.""",
                        default=config_default.statistics_folder,
                        type=str)
    

    ################################
    # Browser Settings

    # TODO Wider web browser and web driver support
    # parser.add_argument('-w', '--web_browser',
    #                     help="""Web browser which will be used by bot.
    #                             Choose from 'Chrome', 'Firefox' """,
    #                     default=config_default.statistics_folder,
    #                     type=str)

    # parser.add_argument('-w', '--web_browser',
    #                     help="""Path to chrome web browser executable.
    #                             Chrome is only one supported for now!!""",
    #                     default=config_default.web_browser,
    #                     type=str)

    parser.add_argument('-wd', '--web_browser_driver',
                        help="Path to chrome web driver.",
                        default=config_default.web_browser_driver,
                        type=str)
    
    parser.add_argument('-hl', '--headless',
                        help="Make chrome headless, means browser's window is not rendered.",
                        default=config_default.verbose,
                        action="store_true")


    ################################
    # Program Behaviour

    parser.add_argument('-v', '--verbose',
                        help="Make console output more verbose.",
                        default=config_default.verbose,
                        action="store_true")

    parser.add_argument('-chf', '--checking_frequency',
                        help="Time (in seconds) between bot tries to work.",
                        default=config_default.checking_frequency,
                        type=int)


    ################################
    # Bot Behaviour
    
    # Chances

    parser.add_argument('--chance_of_change_site',
                        help="""The chance bot has after viewing each post to change site.
                                It's a float number between 0.0 and 1.0""",
                        default=config_default.chance_of_change_site,
                        type=float)

    parser.add_argument('--chance_of_like',
                        help="""The chance bot has when viewing a post to like it.
                                It's a float number between 0.0 and 1.0""",
                        default=config_default.chance_of_like,
                        type=float)

    parser.add_argument('--chance_of_comment',
                        help="""The chance bot has when viewing a post to comment it, if it has been liked earlier.
                                It's a float number between 0.0 and 1.0""",
                        default=config_default.chance_of_comment,
                        type=float)

    parser.add_argument('--chance_of_follow',
                        help="""The chance bot has when viewing a post to follow its author, if it has been liked earlier.
                                It's a float number between 0.0 and 1.0""",
                        default=config_default.chance_of_follow,
                        type=float)

    parser.add_argument('--chance_of_unfollow',
                        help="""The chance bot has when viewing a post to unfollow its author, if it was followed earlier.
                                It's a float number between 0.0 and 1.0""",
                        default=config_default.chance_of_unfollow,
                        type=float)


    # Followings limits

    parser.add_argument('--min_of_followings',
                        help="The minimum number of followed people by bot.",
                        default=config_default.min_of_followings,
                        type=int)

    parser.add_argument('--max_of_followings',
                        help="The maximum number of followed people by bot.",
                        default=config_default.max_of_followings,
                        type=int)


    # Limits per hour

    parser.add_argument('--max_likes_per_hour',
                        help="""The maximum number of likes bot can do per hour.
                                0 means no likes. -1 means unlimited.""",
                        default=config_default.max_likes_per_hour,
                        type=int)

    parser.add_argument('--max_comments_per_hour',
                        help="""The maximum number of comments bot can do per hour.
                                0 means no likes. -1 means unlimited.""",
                        default=config_default.max_comments_per_hour,
                        type=int)

    parser.add_argument('--max_follows_per_hour',
                        help="""The maximum number of follows bot can do per hour.
                                0 means no likes. -1 means unlimited.""",
                        default=config_default.max_follows_per_hour,
                        type=int)

    parser.add_argument('--max_unfollows_per_hour',
                        help="""The maximum number of unfollows bot can do per hour.
                                0 means no likes. -1 means unlimited.""",
                        default=config_default.max_unfollows_per_hour,
                        type=int)


    # Limits per day

    parser.add_argument('--max_likes_per_day',
                        help="""The maximum number of likes bot can do per day.
                                0 means no likes. -1 means unlimited.""",
                        default=config_default.max_likes_per_day,
                        type=int)

    parser.add_argument('--max_comments_per_day',
                        help="""The maximum number of comments bot can do per day.
                                0 means no likes. -1 means unlimited.""",
                        default=config_default.max_comments_per_day,
                        type=int)

    parser.add_argument('--max_follows_per_day',
                        help="""The maximum number of follows bot can do per day.
                                0 means no likes. -1 means unlimited.""",
                        default=config_default.max_follows_per_day,
                        type=int)

    parser.add_argument('--max_unfollows_per_day',
                        help="""The maximum number of unfollows bot can do per day.
                                0 means no likes. -1 means unlimited.""",
                        default=config_default.max_unfollows_per_day,
                        type=int)

    global data
    data = parser.parse_args()


    if data.web_browser_driver == "":
        print("[ERROR]: web_browser_driver parameter wasn't specified in neither config file nor command line arguments.")
        exit()

