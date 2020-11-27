import random, argparse, shutil, datetime
from tools import instagram
from tools.instagram import actions, exceptions
from tools import statistics, config
from pathlib import Path
from tools.logger import Logger


def handle_args():

    # Define the program
    parser = argparse.ArgumentParser(prog="Instagram PyBot",
                                     usage='python main.py <command> <dirpath>',
                                     description="Instagram Bot written in Python and Selenium. It can like, comment, follow and unfollow.")
    parser.version = '0.1.0'

    # Define arguments
    subparsers = parser.add_subparsers(metavar="COMMANDS:", dest="command", required=True)

    init_parser = subparsers.add_parser("init", usage="python main.py init <dirpath>", help="Init a folder with settings for the bot")
    init_parser.set_defaults(func=init)
    init_parser.add_argument("dirpath", help="Path to folder where setting files for the bot will be initiated")

    start_parser = subparsers.add_parser("start", usage="python main.py start <dirpath>", help="Start the bot")
    start_parser.set_defaults(func=start)
    start_parser.add_argument("dirpath", help="Path to folder with bot settings and data") 

    start_parser = subparsers.add_parser("exportdb", usage="python main.py exportdb <dirpath>", help="Export db to csv of the bot")
    start_parser.set_defaults(func=exportdb)
    start_parser.add_argument("dirpath", help="Path to folder with bot settings and data") 

    # Parse arguments
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

    config.check_json_config()

    if config.data.web_browser_driver == "":
        print("[ERROR]: web_browser_driver parameter wasn't specified in neither config file nor command line arguments.")
        exit()

    Logger.getInstance()
    
    while True:
        config.check_json_config()

        if not (datetime.datetime.now().hour > config.data.start_hour and datetime.datetime.now().hour < config.data.end_hour):
            actions.sleep()
            continue

        instagram.actions.driver_init()
        
        # Log In
        instagram.actions.log_in()
        instagram.actions.get_following_count()
        instagram.actions.get_followers_count()

        ActionBlock = False

        def run():
            nonlocal ActionBlock

            try: instagram.actions.like_likelist(3)
            except instagram.exceptions.LimitReached:
                return
            except instagram.exceptions.ActionBlock: 
                actions.change_site_main()
                ActionBlock = True
                return

            SITES = []
            with open(Path(config.data.sites_file), encoding="UTF-8") as f:
                SITES = [line.strip() for line in f.readlines()]

            while len(SITES) > 0:
                site = SITES.pop(random.randint(0, len(SITES)-1))
                instagram.actions.change_site(site)

                try: 
                    instagram.actions.work_on_site()
                except instagram.exceptions.LimitReached:
                    return
                except instagram.exceptions.ActionBlock: 
                    actions.change_site_main()
                    ActionBlock = True
                    return
            
        run()

        if not ActionBlock:
            try: instagram.actions.unfollow_in_profile()
            except instagram.exceptions.ActionBlock:
                instagram.actions.change_site_profile()
                ActionBlock = True
        
        instagram.actions.change_site_profile()
        instagram.actions.log_out()
        instagram.actions.driver_close()

        if ActionBlock:
            config.delete_cookies()

        instagram.actions.sleep()


def exportdb(args):
    if not Path(args.dirpath).exists():
        print("[ERROR] Specified dirpath does not exist!")
        exit()

    config.check_json_config()

    from tools import db
    db.db2csv()


if __name__ == "__main__":
    main()
