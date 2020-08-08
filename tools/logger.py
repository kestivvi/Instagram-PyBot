import threading, time, os
from tools import statistics, config

##################################
# VARIABLES

class BotStatus():
    STARTING_DRIVER = "Starting Driver"
    LOGGING_IN = "Logging In"
    UNFOLLOWING_IN_PROFILE = "Unfollowing in profile list"
    RUNNING = "Running"
    LOGGING_OUT = "Logging Out"
    CLOSING_DRIVER = "Closing Driver"
    SLEEPING = "Sleeping"
    NONE = ""


class _SilentLogger():

    __instance = None

    @staticmethod
    def getInstance():
        if _SilentLogger.__instance == None:
            _SilentLogger()
        return _SilentLogger.__instance

    def __init__(self):
        if _SilentLogger.__instance != None:
            raise Exception("This class is a singleton!")
        _SilentLogger.__instance = self
        
    def set_bot_status(self, status=BotStatus.NONE):
        pass
    
    def get_bot_status(self):
        pass
    
    def set_current_site(self, current_site=""):
        pass

    def get_current_site(self):
        pass
    
    def set_followings(self, followings=""):
        pass

    def get_followings(self):
        pass
    
    def set_followers(self, followers=""):
        pass

    def get_followers(self):
        pass


class Logger():

    __instance = None

    @staticmethod
    def getInstance():
        if config.data.verbose:
            if Logger.__instance == None:
                Logger()
            return Logger.__instance
        else:
            return _SilentLogger.getInstance()


    def __init__(self, status=BotStatus.NONE, current_site=""):
        if Logger.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.bot_status = status
            self.current_site = current_site
            self.followings = ""
            self.followers = ""
            self.thread = threading.Thread(target=self.log, daemon=True)
            self.thread.start()
            Logger.__instance = self

    def set_bot_status(self, status=BotStatus.NONE):
        if status != BotStatus.NONE:
            self.bot_status = status
    
    def get_bot_status(self):
        return self.bot_status
    
    def set_current_site(self, current_site=""):
        self.current_site = current_site

    def get_current_site(self):
        return self.current_site
    

    def set_followings(self, followings=""):
        if followings != "":
            self.followings = followings

    def get_followings(self):
        return self.followings
    
    def set_followers(self, followers=""):
        if followers != "":
            self.followers = followers

    def get_followers(self):
        return self.followers


    def _clear(self):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def log(self):
        while True:
            likes_24h = statistics.get(statistics.Data.LIKES, hours=24)
            comments_24h = statistics.get(statistics.Data.COMMENTS, hours=24)
            follows_24h = statistics.get(statistics.Data.FOLLOWS, hours=24)
            unfollows_24h = statistics.get(statistics.Data.UNFOLLOWS, hours=24)

            likes_24h_max = config.data.max_likes_per_day
            comments_24h_max = config.data.max_comments_per_day
            follows_24h_max = config.data.max_follows_per_day
            unfollows_24h_max = config.data.max_unfollows_per_day

            likes_1h = statistics.get(statistics.Data.LIKES, hours=1)
            comments_1h = statistics.get(statistics.Data.COMMENTS, hours=1)
            follows_1h = statistics.get(statistics.Data.FOLLOWS, hours=1)
            unfollows_1h = statistics.get(statistics.Data.UNFOLLOWS, hours=1)

            likes_1h_max = config.data.max_likes_per_hour
            comments_1h_max = config.data.max_comments_per_hour
            follows_1h_max = config.data.max_follows_per_hour
            unfollows_1h_max = config.data.max_unfollows_per_hour


            self._clear()
            print(f'\t\tLikes\t\tComments\tFollows\t\tUnfollows')
            print('-------------------------------------------------------------------------')
            print(f'Last 24H :\t{likes_24h}\t\t{comments_24h}\t\t{follows_24h}\t\t{unfollows_24h}')
            print(f'MAX 24H : \t{likes_24h_max}\t\t{comments_24h_max}\t\t{follows_24h_max}\t\t{unfollows_24h_max}')
            print('-------------------------------------------------------------------------')
            print(f'Last 1H :\t{likes_1h}\t\t{comments_1h}\t\t{follows_1h}\t\t{unfollows_1h}')
            print(f'MAX 1H : \t{likes_1h_max}\t\t{comments_1h_max}\t\t{follows_1h_max}\t\t{unfollows_1h_max}')
            print('_________________________________________________________________________')
            print()
            print(f'Followings :\t{self.followings}')
            print(f'Followers : \t{self.followers}')
            print()
            print(f'Status:\t\t{self.bot_status}')
            print(f'Current Site:\t{self.current_site}')
            print()

            time.sleep(1)

            