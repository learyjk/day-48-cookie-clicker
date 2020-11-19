from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import time, sleep
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

chrome_driver_path = "/Users/keeganleary/Development/chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

driver.get("http://orteil.dashnet.org/experiments/cookie/")

five_min_timer = time() + 60*5
five_second_timer = time() + 5

def update_money():
    return locale.atoi(driver.find_element_by_id("money").text)

def update_store():
    store = driver.find_elements_by_css_selector("#store b")

    # get a list of items in the shop and their costs. Store as dict.
    d = []
    for item in store:
        if " - " in item.text:
            s = item.text.split(" - ")
            s2 = s[1].split("\n")
            d.append({
                'item': s[0],
                'cost': locale.atoi(s2[0])
            })
    return d

while True:
    # click the cookie
    cookie = driver.find_element_by_id("cookie")
    cookie.click()

    if time() > five_min_timer:
        print(driver.find_element_by_id("cps").text)
        break
    elif time() > five_second_timer:

        store_items = update_store()
        updated_money = update_money()

        # loop from most expensive item and buy if we have enough money
        i = len(store_items) - 1
        while i >= 0:
            if store_items[i]['cost'] < updated_money:
                # need to update the cost after each click!
                item_to_buy = driver.find_element_by_id(f"buy{store_items[i]['item']}")
                item_to_buy.click()
                sleep(0.1)
                store_items = update_store()
                updated_money = update_money()
                sleep(0.1)
            else:
                i -= 1

        # reset the five second timer
        five_second_timer = time() + 5

