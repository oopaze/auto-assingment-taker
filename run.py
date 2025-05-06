from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

from lib.assignment import Assignment 
from lib.checkers import BossPowerAssigmentChecker, LairBossKillAssignmentChecker
from lib.helpers import load_all_more_cards, click_out_for_closing_modal, are_card_lists_equal


driver = webdriver.Firefox()
driver.get("SOME_URL_THAT_WE_WANT_TO_HIDE")

# Wait for the page to load and login
input("Press Enter after logging in...")

checkers = [
    BossPowerAssigmentChecker(),
    LairBossKillAssignmentChecker()
]


CARD_LIST_XPATH = '/html/body/div[1]/div[5]/div/div[2]/div[1]/ul'
CARD_TITLE_XPATH = '/html/body/div[1]/div[5]/div/div[2]/div[1]/ul/li[{0}]/div[2]/div[1]/h3'
CARD_DESCRIPTION_XPATH = '/html/body/div[1]/div[5]/div/div[2]/div[1]/ul/li[{0}]/div[2]/p'
CARD_PRICE_XPATH = '/html/body/div[1]/div[5]/div/div[2]/div[1]/ul/li[{0}]/div[2]/div[3]/p'
CARD_ORDER_BUTTON_XPATH = '/html/body/div[1]/div[5]/div/div[2]/div[1]/ul/li[{0}]/div[2]/div[4]/button[1]'
LOAD_MORE_BUTTON_CSS_SELECTOR = 'div.load-more'


while True:
    card_list = driver.find_element(By.XPATH, CARD_LIST_XPATH)
    card_items = card_list.find_elements(By.TAG_NAME, 'li')

    load_all_more_cards(driver, LOAD_MORE_BUTTON_CSS_SELECTOR)

    for i, card in enumerate(card_items):
        try:
            card_index = i + 1  

            title = card.find_element(By.XPATH, CARD_TITLE_XPATH.format(card_index)).text
            description = card.find_element(By.XPATH, CARD_DESCRIPTION_XPATH.format(card_index)).text
            price_element = card.find_element(By.XPATH, CARD_PRICE_XPATH.format(card_index))
            get_order_button = card.find_element(By.XPATH, CARD_ORDER_BUTTON_XPATH.format(card_index))

            assignment = Assignment(
                title=title,
                description=description,
                price=Assignment.standarize_price(price_element),
                get_order_button=get_order_button
            )

            if assignment.should_click_on_order_button(checkers):
                get_order_button.click()
                click_out_for_closing_modal(driver)
        except Exception as e:
            click_out_for_closing_modal(driver)
            print(f"Error processing card {i}: {e}")
            continue

    next_card_list = driver.find_element(By.XPATH, CARD_LIST_XPATH)
    next_card_items = next_card_list.find_elements(By.TAG_NAME, 'li')

    if are_card_lists_equal(card_items, next_card_items):
        print("No new cards found. Waiting for 5 seconds...")
        sleep(5)
