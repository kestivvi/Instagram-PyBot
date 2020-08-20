from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import time, random, datetime, json
from pathlib import Path
from .. import statistics, config
from ..logger import Logger, BotStatus
from . import exceptions


###############################
# FUNCTIONS


def get_comments():
    comments = []
    with open(Path(config.data.comments_file), 'r', encoding="utf-8") as f:
        comments = [line.strip() for line in f.readlines()]
    return comments


def get_emojis():
    emojis = []
    with open(Path(config.data.emojis_file), 'r', encoding="utf-8") as f:
        emojis = [line.strip() for line in f.readlines()]
    return emojis


def get_following_whitelist():
    whitelist = []
    with open(Path(config.data.following_whitelist), 'r', encoding="utf-8") as f:
        whitelist = [line.strip() for line in f.readlines()]
    return whitelist


def check_restrictness():
    try:
        driver.find_element_by_css_selector("div[role=dialog]")
        ok_button = driver.find_element_by_css_selector("button.HoLwm")
        time.sleep(random.uniform(1,3))
        ok_button.click()

        statistics.update(statistics.Data.ERRORS, message="Instagram ActionBlock error")
        
        raise exceptions.ActionBlock
    except NoSuchElementException:
        pass


def type_in(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2))


def sleep(seconds, interval=1):
    started_at = datetime.datetime.now()
    to = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
    logger = Logger.getInstance()
    
    while seconds > 0:
        seconds -= interval
        remaining = to - datetime.datetime.now()
        message = f"Sleeping : Started at {started_at.strftime('%H:%M:%S')}. Waiting to {to.strftime('%H:%M:%S')}. Remaining time: {str(remaining).split('.')[0]}"
        logger.set_bot_status(message)    
        time.sleep(interval)


def remove_duplicates(arr):
    result = []
    for item in arr:
        if item not in result:
            result.append(item)

    return result


def driver_init():
    logger = Logger.getInstance()
    logger.set_bot_status(BotStatus.STARTING_DRIVER)

    if config.data.web_browser_driver == "" or not Path(config.data.web_browser_driver).exists():
        print("[ERROR]: Path to chrome webdriver not found. Check your config.json file.")

    global driver
    if config.data.headless:
        options = webdriver.chrome.options.Options()
        options.headless = True
        driver = webdriver.Chrome(Path(config.data.web_browser_driver), options=options)
    else:
        driver = webdriver.Chrome(Path(config.data.web_browser_driver))

    driver.implicitly_wait(1)


def driver_close():
    logger = Logger.getInstance()
    logger.set_bot_status(BotStatus.CLOSING_DRIVER)
    driver.quit()


def log_in():
    logger = Logger.getInstance()
    logger.set_bot_status(BotStatus.LOGGING_IN)

    # Loading main instagram page to log in
    loaded = False
    while not loaded:
        change_site_main()
        
        try:
            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
        except:
            continue
        try:
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
        except:
            continue
        loaded = True
    
    time.sleep(random.uniform(0.5,2))
    
    # Typing in credentials and logging in
    credentials = config.get_credentials()
    type_in(username_field, credentials[0])
    time.sleep(random.uniform(0.5,2))
    type_in(password_field, credentials[1])
    del credentials
    time.sleep(random.uniform(0.5,2))
    password_field.send_keys(Keys.RETURN)

    # Checking if credentials has been correct
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "slfErrorAlert"))
        )
        print("[ERROR]: Wrong Credentials! Check if username and password are correct!")
        raise exceptions.WrongCredentials
    except:
        pass

    # Waiting for instagram to load up
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "s4Iyt"))
        )
    except:
        print("[ERROR]: Page cannot load")
        exit()

    # Ommitting instagram question dialog about saving credentials
    change_site_main()


def get_username():
    
    # Check cache
    filename = Path(config.data.data_folder) / "usernames.json"
    usernames = {}
    login_name = config.get_credentials()[0]

    if filename.exists():
        with open(filename, "r", encoding="UTF-8") as f:
            usernames = json.load(f)
            if login_name in usernames:
                return usernames[login_name]

    # Find username
    change_site_profile_manually()
    usernames[login_name] = driver.find_element_by_class_name("_7UhW9").text.strip()

    # Append to cache
    with open(filename, "w", encoding="UTF-8") as f:
        json.dump(usernames, f)

    return usernames[login_name]


def get_following_count():
    change_site_profile()
    time.sleep(random.uniform(0.5,2))
    following_div = driver.find_element_by_css_selector('a[href*="following"]')
    global followings
    followings = int(following_div.find_element_by_css_selector("span.g47SY").text)

    logger = Logger.getInstance()
    logger.set_followings(followings)


def log_out():

    logger = Logger.getInstance()
    logger.set_bot_status(BotStatus.LOGGING_OUT)

    profile_div = driver.find_element_by_css_selector("div.Fifk5 > span[role=link]")
    profile_div.click()
    time.sleep(random.uniform(0.5,2))
    log_out_div = driver.find_element_by_css_selector("div._01UL2 > div[role=button]")
    log_out_div.click()

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
    except:
        pass
    logger.set_current_site("")


def change_site_hashtag(name):
    while name[0] == '#':
        name = name[1:]

    url = f"https://www.instagram.com/explore/tags/{name}/"
    logger = Logger.getInstance()
    logger.set_current_site(url)

    driver.get(url)


def change_site_person(name):
    url = f"https://www.instagram.com/{name}/"
    logger = Logger.getInstance()
    logger.set_current_site(url)

    driver.get(url)


def change_site_main():
    url = "https://www.instagram.com"
    logger = Logger.getInstance()
    logger.set_current_site(url)

    driver.get(url)

    # Omitting instagram dialog about notifications, if present
    try:
        not_now_button = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[role=dialog] button.HoLwm"))
            )
        time.sleep(random.uniform(0.5,2))
        not_now_button.click()
    except:
        pass


def change_site_profile():
    url = f"https://www.instagram.com/{get_username()}/"
    driver.get(url)
    logger = Logger.getInstance()
    logger.set_current_site(url)


def change_site_profile_manually():
    time.sleep(random.uniform(0.5,2))
    # Clicking on the profile image
    profile_div = driver.find_element_by_css_selector("div.Fifk5 > span[role=link]")
    profile_div.click()
    time.sleep(random.uniform(0.5,2))
    # Clicking first option "profile"
    try:
        profile_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div._01UL2 > a.-qQT3"))
            )
        time.sleep(random.uniform(0.5,2))
        profile_button.click()
    except:
        pass
    
    # Be sure page is loaded
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "be6sR")))
    except NoSuchElementException:
        pass
    
    url = driver.current_url
    logger = Logger.getInstance()
    logger.set_current_site(url)

def change_site(name=""):
    if name[0] == '#':
        change_site_hashtag(name)
    elif name == "":
        change_site_main()
    elif name == "profile":
        change_site_profile()
    else:
        change_site_person(name)


def like(post):
    is_liked = bool(post.find_elements_by_css_selector('span.fr66n button.wpO6b svg[fill="#ed4956"]'))
    
    if not is_liked:
        try:
            like_button = post.find_element_by_css_selector("span.fr66n button.wpO6b")
            like_button.click()

            check_restrictness()

            statistics.update(statistics.Data.LIKES)
            return True
        except NoSuchElementException:
            return False
    return False


def comment(post):
    try:
        comment_button = post.find_element_by_class_name("_15y0l")
        comment_button.click()
        
        textarea = post.find_element_by_class_name("Ypffh")
    
        text = random.choice(get_comments()) + " "
        for _ in range(random.randint(0,3)):
            text += random.choice(get_emojis())

        text = text.strip()

        textarea.click()
        textarea = post.find_element_by_class_name("Ypffh")
        type_in(textarea, text)
        textarea.send_keys(Keys.RETURN)

        error = bool(driver.find_elements_by_class_name("HGN2m"))
        if error:
            statistics.update(statistics.Data.ERRORS, message="Couldn't post comment")
            return False

        check_restrictness()

        statistics.update(statistics.Data.COMMENTS)
        return True
    except NoSuchElementException:
        return False


def follow(post):
    is_followed = bool(post.find_elements_by_css_selector("div.bY2yH button._8A5w5"))

    if not is_followed:
        try:
            follow_button = driver.find_element_by_css_selector("div.bY2yH button.y3zKF")
            follow_button.click()

            check_restrictness()

            statistics.update(statistics.Data.FOLLOWS)
            global followings
            followings += 1
            return True
        except NoSuchElementException:
            return False
    return False


def unfollow(post):
    is_followed = bool(post.find_elements_by_css_selector("div.bY2yH button._8A5w5"))

    if is_followed:
        try:
            follow_button = driver.find_element_by_css_selector("div.bY2yH button._8A5w5")
            follow_button.click()
            red_unfollow_button = driver.find_element_by_class_name("-Cab_")
            red_unfollow_button.click()

            check_restrictness()

            statistics.update(statistics.Data.UNFOLLOWS)
            global followings
            followings -= 1
            return True
        except NoSuchElementException:
            return False
    return False


def get_followers_count():
    change_site_profile()
    followers_div = driver.find_element_by_css_selector('a[href*="followers"]')
    time.sleep(random.uniform(0.5,2))
    followers = int(followers_div.find_element_by_css_selector("span.g47SY").text)
    logger = Logger.getInstance()
    logger.set_followers(followers)

    return followers

def scroll_down(list_div):
    count = 0
    div_list = list_div.find_elements_by_tag_name("li")
    while len(div_list) > count :
        count = len(div_list)

        driver.execute_script(f'document.getElementsByClassName("PZuss")[0].lastChild.scrollIntoView()')
        time.sleep(random.uniform(0.5,2))

        # Wait for content to load
        last_child = driver.find_element_by_css_selector(".PZuss:last-child")
        try:
            last_child = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".PZuss:last-child"))
                )
        except:
            pass

        time.sleep(random.uniform(0.5,2))
        while last_child != driver.find_element_by_css_selector(".PZuss:last-child"):
            time.sleep(random.uniform(0.5,2))
            last_child = driver.find_element_by_css_selector(".PZuss:last-child")

        div_list = list_div.find_elements_by_tag_name("li")

def get_followers():
    change_site_profile()
    time.sleep(random.uniform(0.5,2))

    followers_button = driver.find_element_by_css_selector('a[href*="followers"]')
    followers_button.click()
    time.sleep(random.uniform(0.5,2))

    # Find div where all followers are in list
    followers_list_div = driver.find_element_by_class_name("PZuss")

    scroll_down(followers_list_div)

    followers_list = followers_list_div.find_elements_by_tag_name("li")
    
    # Get the names
    followers_names = []
    for div in followers_list:
        followers_names.append(div.find_element_by_class_name("FPmhX").text.strip())

    time.sleep(random.uniform(0.5,2))

    return followers_names


def unfollow_in_profile():

    logger = Logger.getInstance()
    logger.set_bot_status(BotStatus.UNFOLLOWING_IN_PROFILE)

    # Get count of people you're following
    global followings
    get_following_count()

    # Check limit
    unfollow_limit = not (config.data.chance_of_unfollow > 0 
        and statistics.get(statistics.Data.UNFOLLOWS, hours=1) < config.data.max_unfollows_per_hour 
        and statistics.get(statistics.Data.UNFOLLOWS, hours=24) < config.data.max_unfollows_per_day
        and followings > config.data.min_of_followings)

    if unfollow_limit:
        return
    
    if config.data.unfollow_non_followers_first:
        followers_names = get_followers()
    
    change_site_profile()
    time.sleep(random.uniform(0.5,2))

    # Find button
    following_div = driver.find_element_by_css_selector('a[href*="following"]')
    time.sleep(random.uniform(0.5,2))
    following_div.click()

    # Find div where all followers are in list
    following_list_div = driver.find_element_by_class_name("PZuss")

    scroll_down(following_list_div)

    following_list = following_list_div.find_elements_by_tag_name("li")

    # Apply whitelist
    whitelist = get_following_whitelist()
    new_following_list = []
    for div in following_list:
        name = div.find_element_by_class_name("FPmhX").text.strip()
        if name not in whitelist:
            new_following_list.append(div)
    
    following_list = new_following_list

    # Make a list of nonfollowings
    if config.data.unfollow_non_followers_first:
        non_followings = []
        for div in following_list:
            name = div.find_element_by_class_name("FPmhX").text.strip()
            if name not in followers_names:
                non_followings.append(div)

    # While limit is not reached unfollow
    while not unfollow_limit:

        # If unfollow_not_followers_first find following that doesn't follow you, else random
        if config.data.unfollow_non_followers_first and len(non_followings) > 0:
            following = non_followings.pop(random.randint(0, len(non_followings)-1))
        else:
            following = following_list.pop(random.randint(0, len(following_list)-1))
        
        # Find unfollow button
        unfollow_button = following.find_element_by_tag_name("button")
        unfollow_button.click()
        time.sleep(random.uniform(0.5,2))

        # Find confirmation unfollow button
        red_unfollow_button = driver.find_element_by_class_name("-Cab_")
        red_unfollow_button.click()
        time.sleep(random.uniform(0.5,2))

        check_restrictness()
        
        # Update statistics
        statistics.update(statistics.Data.UNFOLLOWS)
        followings -= 1
        
        # Check config and limit
        config.check_json_config()
        unfollow_limit = not (config.data.chance_of_unfollow > 0 
            and statistics.get(statistics.Data.UNFOLLOWS, hours=1) < config.data.max_unfollows_per_hour 
            and statistics.get(statistics.Data.UNFOLLOWS, hours=24) < config.data.max_unfollows_per_day
            and followings > config.data.min_of_followings)
    

def work_on_site(post_limit=-1, like_chance=1, comment_chance=1, follow_chance=1, unfollow_chance=1):

    logger = Logger.getInstance()
    logger.set_bot_status(BotStatus.RUNNING)

    gonna_change_site = False

    post_nr = 0
    posts = []
    # While ERROR or ChangeSite or LimitReached
    while not gonna_change_site and (post_limit == -1 or post_nr < post_limit):
        config.check_json_config()

        posts += driver.find_elements_by_class_name("v1Nh3")
        posts = remove_duplicates(posts)
        post = posts[post_nr]
        time.sleep(random.uniform(0.5,2))

        try:
            post.click()
        except:
            post_nr += 1
            continue
        time.sleep(random.uniform(0.5,2))

        # If post not loaded
        try: 
            post_dialog = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "M9sTE")))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "fr66n")))
        except:
            driver.find_element_by_tag_name("body").send_keys(Keys.ESCAPE)
            post_nr += 1
            time.sleep(random.uniform(0.5,2))
            continue

        like_limit = ((config.data.max_likes_per_hour != -1 and statistics.get(statistics.Data.LIKES, hours=1) >= config.data.max_likes_per_hour)
                  or (config.data.max_likes_per_day != -1 and statistics.get(statistics.Data.LIKES, hours=24) >= config.data.max_likes_per_day))
        comment_limit = ((config.data.max_comments_per_hour != -1 and statistics.get(statistics.Data.COMMENTS, hours=1) >= config.data.max_comments_per_hour)
                     or (config.data.max_comments_per_day != -1 and statistics.get(statistics.Data.COMMENTS, hours=24) >= config.data.max_comments_per_day))
        follow_limit = ((config.data.max_follows_per_hour != -1 and statistics.get(statistics.Data.FOLLOWS, hours=1) >= config.data.max_follows_per_hour)
                    or (config.data.max_follows_per_day != -1 and statistics.get(statistics.Data.FOLLOWS, hours=24) >= config.data.max_follows_per_day)
                    or followings >= config.data.max_of_followings)
        unfollow_limit = ((config.data.max_unfollows_per_hour != -1 and statistics.get(statistics.Data.UNFOLLOWS, hours=1) >= config.data.max_unfollows_per_hour)
                      or (config.data.max_unfollows_per_hour != -1 and statistics.get(statistics.Data.UNFOLLOWS, hours=24) >= config.data.max_unfollows_per_hour))
        
        def do_stuff():
            chance = random.random()

            # like
            if not like_limit and chance < config.data.chance_of_like and chance < like_chance:
                like(post_dialog)
                time.sleep(random.uniform(0.5,2))

            # if liked:
                # comment
                if not comment_limit and chance < config.data.chance_of_comment and chance < comment_chance:
                    comment(post_dialog)
                    time.sleep(random.uniform(1,3))

                # follow
                if not follow_limit and chance < config.data.chance_of_follow and chance < follow_chance:
                    follow(post_dialog)
                    time.sleep(random.uniform(0.5,2))

            else:
                # unfollow
                if not unfollow_limit and chance < config.data.chance_of_unfollow and chance < unfollow_chance:
                    unfollow(post_dialog)
                    time.sleep(random.uniform(0.5,2))
        
        try: do_stuff()
        except ElementNotInteractableException: pass

        # Back to site
        driver.find_element_by_tag_name("body").send_keys(Keys.ESCAPE)
        post_nr += 1

        if post_nr > 10 and random.random() < config.data.chance_of_change_site:
            gonna_change_site = True
        
        if like_limit:
            raise exceptions.LimitReached

        time.sleep(random.uniform(0.5,2))
    return False


def like_likelist(how_many_post=3):
    likelist = []

    with open(config.data.likelist, "r", encoding="UTF-8") as f:
        likelist = [line.strip() for line in f.readlines()]
    
    while len(likelist) > 0:
        site = likelist.pop(random.randrange(0, len(likelist)))
        change_site(site)
        work_on_site(how_many_post, like_chance=1, comment_chance=0, follow_chance=0, unfollow_chance=0)


def work_on():
    site = False
    main = False

    try:
        site = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CLASS_NAME, "v1Nh3"))
            )
        site = bool(site)
    except:
        pass

    try:
        main = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CLASS_NAME, "M9sTE"))
            )
        main = bool(main)
    except:
        pass

    if site:
        work_on_site()
    # elif main:
    #     like_on_main()
    # else:
    #     print("[ERROR]", "It's not site neither main")

