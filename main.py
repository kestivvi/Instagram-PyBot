from selenium.webdriver.common.keys import Keys
import random, time
from tools import instagram
from tools.instagram import actions, errors
from tools import statistics, config
from path import Path
from tools.logger import Logger


def main():
    config.handle_args()
    Logger()
    
    # While True
    while True:
        config.handle_args()
        instagram.actions.driver_init()

        # Log In
        instagram.actions.log_in()

        try: instagram.actions.unfollow_in_profile()
        except instagram.errors.ActionBlock:
            pass

        SITES = []
        with open(Path(config.data.sites_file), encoding="UTF-8") as f:
            SITES = [line.strip() for line in f.readlines()]

        while len(SITES) > 0:
            site = SITES.pop(random.randint(0, len(SITES)-1))
            instagram.actions.change_site(site)

            try: 
                limit_reached = instagram.actions.work_on_site()
                if limit_reached:
                    break
            except instagram.errors.ActionBlock: 
                instagram.actions.driver.find_element_by_tag_name("body").send_keys(Keys.ESCAPE)
                time.sleep(random.uniform(0.5,2))
                break
            
        instagram.actions.log_out()
        instagram.actions.driver_close()
        instagram.actions.sleep(config.data.checking_frequency)

main()
