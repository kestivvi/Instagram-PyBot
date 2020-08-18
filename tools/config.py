from collections import namedtuple
import argparse, json, functools
from path import Path



def check_json_config(bot_folder):
    """
        Load or refresh settings from config.json

        
        :param bot_folder: Path to folder with config.json and other bot data
    """
    
    bot_folder = Path(bot_folder)

    if bot_folder.exists():
        json_path = bot_folder / "config.json"
       
        if json_path.exists():
            with open(json_path) as f:

                # Convert dict from json to namespace object
                new_data = argparse.Namespace(**json.load(f))

                new_data.data_folder        = bot_folder / "data/"
                new_data.credentials_file   = bot_folder / "secret.txt"
                new_data.sites_file         = bot_folder / "sites.txt"
                new_data.comments_file      = bot_folder / "comments.txt"
                new_data.emojis_file        = bot_folder / "emojis.txt"

                return new_data
        else:
            print("[ERROR] config.json does not exist in specified bot folder!")
    else:
        print("[ERROR] Specified bot folder does not exist!")


def handle_args():

    parser = argparse.ArgumentParser(prog="Instagram PyBot",
                                     usage='%(prog)s [options]',
                                     description="""Instagram Bot written in Python and Selenium.
                                                    It can like, comment, follow and unfollow.""")
    parser.version = '0.1.0'

    parser.add_argument('-bf', '--bot_folder',
                        help="""Path to folder with bot settings and data.""",
                        required=True,
                        type=str)

    global data
    data = check_json_config(parser.parse_args().bot_folder)

    if data.web_browser_driver == "":
        print("[ERROR]: web_browser_driver parameter wasn't specified in neither config file nor command line arguments.")
        exit()


def get_credentials():

    if not data.credentials_file.exists():
        print("[ERROR]: File with credentials is not exist")
        exit()

    username = ""
    password = ""
    
    with open(data.credentials_file, 'r', encoding="utf-8") as f:
        lines = f.readlines()
        username = lines[0].strip()
        password = lines[1].strip()

    if username == "" or password == "":
        print("[ERROR]: File with credentials is empty. First line expected login. Second line expected password.")
        exit()

    return (username, password)

