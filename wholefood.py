#!/usr/bin/python3

# This script checkout Wholefood market carts automatically.

import logging
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import amazon
import args
import driver

def main():
    parser = args.create_parser()
    parser.add_argument("--email", type=str, help="Amazon account email")
    parser.add_argument("--password", type=str, help="Amazon account password")
    a = parser.parse_args()

    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(message)s',
        level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

    try:
        d = driver.create(a.selenium_driver, a.headless, a.private, a.user_agent)
        d.set_window_size(640, 480)
        d.implicitly_wait(a.short_timeout_secs)
        amazon.signin(d, a.email, a.password, a.short_timeout_secs, a.long_timeout_secs)

        while True:
            try:
                logging.info("Loading localmarket and checking out...")
                d.get("https://www.amazon.com/cart/localmarket")
                el = WebDriverWait(d, a.long_timeout_secs).until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "input[value='Proceed to checkout']")))
                el.click()

                while True:
                    el = WebDriverWait(d, a.long_timeout_secs).until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR,
                         "[name=proceedToCheckout], #subsContinueButton, .ufss-date-select-toggle-container button")))
                    if el.get_attribute("name") == "proceedToCheckout":
                        logging.info("Proceed to checkout...")
                        el = WebDriverWait(d, a.short_timeout_secs).until(EC.element_to_be_clickable(
                            (By.NAME, "proceedToCheckout")))
                        el.click()
                        WebDriverWait(d, a.long_timeout_secs).until(EC.staleness_of(el))
                    elif el.get_attribute("id") == "subsContinueButton":
                        logging.info("Will allow substitution.")
                        el = WebDriverWait(d, a.short_timeout_secs).until(EC.element_to_be_clickable(
                            (By.ID, "subsContinueButton")))
                        el.click()
                        WebDriverWait(d, a.long_timeout_secs).until(EC.staleness_of(el))
                    else:
                        break

                dates = d.find_elements_by_css_selector(".ufss-date-select-toggle-container")
                logging.info("Checking %d dates..." % len(dates))
                for date in dates:
                    btn = date.find_element_by_tag_name("button")
                    date_str = btn.get_attribute("name")
                    try:
                        date.find_element_by_class_name("a-button-unavailable")
                        logging.warning("%s not available." % date_str)
                    except NoSuchElementException:
                        logging.info("Will use %s." % date_str)
                        try:
                            date.find_element_by_class_name("a-button-selected")
                        except NoSuchElementException:
                            btn.click()
                        time.sleep(1)
                        slot_ctns = d.find_elements_by_class_name("ufss-slot-container")
                        for index, slot_ctn in enumerate(slot_ctns, start=1):
                            time_str = slot_ctn.find_element_by_class_name(
                                "ufss-aok-offscreen").get_attribute("innerText")
                            price_str = slot_ctn.find_element_by_class_name(
                                "ufss-slot-price-text").get_attribute("innerText")
                            logging.info("Found slot '%s', price is '%s'." % (time_str, price_str))
                            if price_str == "FREE":
                                logging.info("Will use %s." % time_str)
                                btn = WebDriverWait(d, a.short_timeout_secs).until(
                                    EC.element_to_be_clickable(
                                        (By.CSS_SELECTOR,
                                        ".ufss-slot-container:nth-child(%d) button" % index)))
                                d.execute_script("arguments[0].scrollIntoView();", btn)
                                btn.click()
                                WebDriverWait(d, a.short_timeout_secs).until(EC.element_to_be_clickable(
                                    (By.CSS_SELECTOR, "input[type=submit]"))).click()
                                WebDriverWait(d, a.long_timeout_secs).until(EC.element_to_be_clickable(
                                    (By.CSS_SELECTOR, "#order-summary-container #continue-top"))).click()
                                WebDriverWait(d, a.long_timeout_secs).until(EC.element_to_be_clickable(
                                    (By.NAME, "placeYourOrder1"))).click()
                                return
            except TimeoutException:
                logging.warning("Timeout. Will retry")
            logging.info("Sleep before retry.")
            time.sleep(a.long_timeout_secs)
                   
    except TimeoutException:
        logging.warning("Timeout.")
    finally:
        pass
        #d.quit()

if __name__ == "__main__":
    main()
