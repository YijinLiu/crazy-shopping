import logging
from typing import Optional

from selenium.webdriver.remote.webdriver import WebDriver
from selenium import webdriver

def create(name: str, headless: bool = True, private: bool = True,
           user_agent: str = "") -> Optional[WebDriver]:
    browser_log_file = "/tmp/selenium.log"
    if name == "firefox":
        logging.info("Starting Firefox...")
        from selenium.webdriver.firefox.options import Options
        options = Options()
        options.set_headless(headless=headless)
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('dom.webdriver.enabled', False)
        if private:
            firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
        if user_agent:
            firefox_profile.set_preference("general.useragent.override", user_agent)
        return webdriver.Firefox(firefox_profile=firefox_profile, options=options,
                                 service_log_path=browser_log_file)

    if name == "chrome":
        logging.info("Starting Chrome...")
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        if private:
            chrome_options.add_argument("--incognito")
        if user_agent:
            chrome_options.add_argument("user-agent=" + user_agent)
        return webdriver.Chrome(chrome_options=chrome_options, log_path=browser_log_file)

    logging.info("Unknown Selenium driver '%s'!" % name)
    return None
