import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import Firefox
from selenium.webdriver.remote.webelement import WebElement

CARD_LOAD_WAIT_TIME = 5 
LOAD_MORE_WAIT_TIME = 5


def load_all_more_cards(driver: Firefox, load_more_button_css_selector, timeout=LOAD_MORE_WAIT_TIME):
    """
    Keep clicking the 'Load More' button until it's no longer found.
    """
    while True:
        try:
            # Wait until the button is clickable
            load_more_button = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, load_more_button_css_selector))
            )
            load_more_button.click()
            time.sleep(CARD_LOAD_WAIT_TIME)  # wait for cards to load after clicking

        except (TimeoutException, NoSuchElementException):
            print("No more 'Load More' button available.")
            break


def click_out_for_closing_modal(driver: Firefox, timeout=LOAD_MORE_WAIT_TIME):
    """
    Click outside of the modal to close it.
    """
    try:
        # Wait for the modal to be present
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".mobile-panel-popup__close"))
        )
        # Click outside the modal to close it
        driver.find_element(By.CSS_SELECTOR, ".mobile-panel-popup__close").click()
    except (TimeoutException, NoSuchElementException):
        print("No modal found or unable to click outside of it.")



def are_card_lists_equal(list1: list[WebElement], list2: list[WebElement]) -> bool:
    """
    Compara duas listas de elementos <li> retornadas pelo Selenium.
    Considera iguais se tiverem o mesmo tamanho e o mesmo conteúdo textual, na mesma ordem.
    """
    if len(list1) != len(list2):
        return False

    for el1, el2 in zip(list1, list2):
        if el1.text.strip() != el2.text.strip():
            return False

    return True