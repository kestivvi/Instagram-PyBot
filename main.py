from selenium.webdriver.common.keys import Keys
import random, time, argparse, shutil
from tools import instagram
from tools.instagram import actions, exceptions
from tools import statistics, config
from path import Path
from tools.logger import Logger


def handle_args():
    parser = argparse.ArgumentParser(prog="Instagram PyBot",
                                     usage='%(prog)s [options]',
                                     description="""Instagram Bot written in Python and Selenium.
                                                    It can like, comment, follow and unfollow.""")
    parser.version = '0.1.0'

    subparsers = parser.add_subparsers(help="commands")

    init_parser = subparsers.add_parser("init", help="Init a folder with settings for bot")
    init_parser.set_defaults(func=init)
    init_parser.add_argument("dirpath", help="Path to folder where setting files for bot will be initiated")

    start_parser = subparsers.add_parser("start", help="Start a bot")
    start_parser.set_defaults(func=start)
    start_parser.add_argument("dirpath", help="Path to folder with bot settings and data") 

    args = parser.parse_args()

    config.set_dirpath(args.dirpath)

    return args


def main():
    args = handle_args()

    # Start init or start function
    args.func(args)


def init(args):
    if Path(args.dirpath).exists():

        answer = input("Specified dirpath already exists in filesystem. All files from this folder will be deleted and replaced by default settings.\nDo you want to continue? y/[n]: ").strip().lower()

        if answer == 'y' or answer == 'yes':
            shutil.rmtree(args.dirpath)
        else:
            exit()
    
    shutil.copytree(Path(__file__).parent / "sample", args.dirpath)

    

def start(args):
    if not Path(args.dirpath).exists():
        print("[ERROR] Specified dirpath does not exist!")
        exit()

    config.check_json_config(args.dirpath)

    if config.data.web_browser_driver == "":
        print("[ERROR]: web_browser_driver parameter wasn't specified in neither config file nor command line arguments.")
        exit()

    Logger.getInstance()
    
    while True:
        config.check_json_config(args.dirpath)
        instagram.actions.driver_init()

        # Log In
        instagram.actions.log_in()
        instagram.actions.get_following_count()
        instagram.actions.get_followers_count()

        SITES = []
        with open(Path(config.data.sites_file), encoding="UTF-8") as f:
            SITES = [line.strip() for line in f.readlines()]

        while len(SITES) > 0:
            site = SITES.pop(random.randint(0, len(SITES)-1))
            instagram.actions.change_site(site)

            try: 
                instagram.actions.work_on_site()
            except instagram.exceptions.LimitReached:
                break
            except instagram.exceptions.ActionBlock: 
                instagram.actions.driver.find_element_by_tag_name("body").send_keys(Keys.ESCAPE)
                time.sleep(random.uniform(0.5,2))
                break
        
        try: instagram.actions.unfollow_in_profile()
        except instagram.exceptions.ActionBlock:
            pass
            
        instagram.actions.log_out()
        instagram.actions.driver_close()
        instagram.actions.sleep(config.data.checking_frequency)

main()
