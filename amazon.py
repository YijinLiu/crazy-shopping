import logging
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def handle_captcha(driver: WebDriver):
    pass

def signin(driver: WebDriver, email: str, password: str, short_timeout_secs: int = 10,
           long_timeout_secs: int = 20):
    logging.info("Loading Amazon home page ...")
    driver.get("https://www.amazon.com/")
    el = WebDriverWait(driver, long_timeout_secs).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "#nav-link-accountList, #captchacharacters")))
    if el.get_attribute('id') == "captchacharacters":
        while True:
            img = driver.find_element_by_css_selector("div.a-text-center > img")
            captcha_url = img.get_attribute("src")
            captcha = input("Please enter the captcha code in '%s': " % captcha_url)
            if captcha:
                el.click()
                el.send_keys(captcha)
                driver.find_element_by_css_selector("button[type=submit]").click()
                try:
                    WebDriverWait(driver, short_timeout_secs).until(EC.staleness_of(el))
                    break
                except TimeoutException:
                    pass
                # Refresh to load a diferent captcha code.
                driver.refresh()
                el = WebDriverWait(driver, long_timeout_secs).until(
                    EC.element_to_be_clickable((By.ID, "captchacharacters")))

        logging.info("Wait for signin page...")
        el = WebDriverWait(driver, long_timeout_secs).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#nav-link-accountList")))

    logging.info("Loading signin page...")
    href = el.get_attribute("href")
    if not href.startswith("https://www.amazon.com/ap/signin?"):
        logging.info("Already signed in.")
        return
    el.click()
    WebDriverWait(driver, long_timeout_secs).until(EC.staleness_of(el))

    if email and password:
        logging.info("Entering email ...")
        el = WebDriverWait(driver, short_timeout_secs).until(
            EC.element_to_be_clickable((By.ID, "ap_email")))
        el.click()
        el.send_keys(email)
        WebDriverWait(driver, short_timeout_secs).until(
            EC.element_to_be_clickable((By.ID, "continue"))).click()
        WebDriverWait(driver, long_timeout_secs).until(EC.staleness_of(el))

        logging.info("Entering password ...")
        el = WebDriverWait(driver, short_timeout_secs).until(
            EC.element_to_be_clickable((By.ID, "ap_password")))
        el.click()
        el.send_keys(password)
        driver.find_element_by_name("rememberMe").click()
        WebDriverWait(driver, short_timeout_secs).until(
            EC.element_to_be_clickable((By.ID, "signInSubmit"))).click()
        WebDriverWait(driver, long_timeout_secs).until(EC.staleness_of(el))
    else:
        logging.info("Please sign in Amazon...")
        while True:
            time.sleep(3)
            try:
                el = driver.find_element_by_id("nav-link-accountList")
                href = el.get_attribute("href")
                if not href.starts_with("https://www.amazon.com/ap/signin?"):
                    break
            except NoSuchElementException:
                pass

    url = driver.current_url
    logging.info("Loaded '%s'." % url)
