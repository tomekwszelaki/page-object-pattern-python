from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from pages.flight_payment_page import FlightPaymentPage


class FlightOptionsPage(object):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)
        self.check_out_btn = (By.CSS_SELECTOR, '.button-next button')
        self.popup_reject_seats_btn = (By.CSS_SELECTOR, '.seat-prompt-popup-footer .core-btn-ghost')

    def element(self, locator):
        return self.driver.find_element(*locator)

    def is_ready(self):
        self.wait.until(element_to_be_clickable(self.check_out_btn))

    def submit(self):
        self.element(self.check_out_btn).click()
        self.wait.until(element_to_be_clickable(self.popup_reject_seats_btn)).click()
        return FlightPaymentPage(self.driver)
