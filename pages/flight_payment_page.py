from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from pages.log_in_page import LogInPage
from config import users
import string
import random


class FlightPaymentPage(object):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.log_in_btn = (By.CSS_SELECTOR, 'button[ui-sref="login"]')
        self.passenger_rows = (By.CSS_SELECTOR, 'div[passengers-form] .row')
        self.passenger_title = (By.CSS_SELECTOR, '.payment-passenger-title select')
        self.passenger_first_name = (By.CSS_SELECTOR, '.payment-passenger-first-name input')
        self.passenger_last_name = (By.CSS_SELECTOR, '.payment-passenger-last-name input')
        self.title_select = None
        self.terms_tick = (By.CSS_SELECTOR, '.terms input[name="acceptPolicy"]')
        self.pay_now_btn = (By.CSS_SELECTOR, '.cta button')

        # card details
        self.card_number = (By.CSS_SELECTOR, 'payment-method-card input[name="cardNumber"]')
        self.card_type = (By.CSS_SELECTOR, 'payment-method-card select[name="cardType"]')
        self.card_expiry_month = (By.CSS_SELECTOR, 'payment-method-card select[name="expiryMonth"]')
        self.card_expiry_year = (By.CSS_SELECTOR, 'payment-method-card select[name="expiryYear"]')
        self.card_cvv = (By.CSS_SELECTOR, 'payment-method-card input[name="securityCode"]')
        self.cardholder = (By.CSS_SELECTOR, 'payment-method-card input[name="cardHolderName"]')

        # billing address
        self.address_line_1 = (By.CSS_SELECTOR, 'div[name="sa.name"] input[name="sa.nameAddressLine1"]')
        self.address_city = (By.CSS_SELECTOR, 'div[name="sa.name"] input[name="sa.nameCity"]')

        # error prompt
        self.error_section = (By.CSS_SELECTOR, 'prompt[text-title="common.components.payment_forms.error_title"]')
        self.error_section_msg = (By.CSS_SELECTOR, 'prompt[text-title="common.components.payment_forms.error_title"] .info-text')

    def element(self, locator):
        return self.driver.find_element(*locator)

    def is_ready(self):
        # using errors for branching is an anti pattern, but with selenium I don't think we can do anything else
        try:
            self.wait.until(element_to_be_clickable(self.log_in_btn))
        except NoSuchElementException as e:
            # we are logged in, so let's do nothing
            pass
        else:
            self.element(self.log_in_btn).click()
            return self.log_in_if_necessary()

    def log_in_if_necessary(self):
        log_in_page = LogInPage(self.driver)
        log_in_page.is_ready()
        log_in_page.log_in(users["test_user_1"], remember_me=False)
        return self

    def is_logged_in(self):
        self.wait.until(visibility_of_element_located(self.passenger_first_name))

    def _fill_in_older_passegers_details(self, row):
        self.surname = "Doe" + ''.join(random.sample(string.ascii_lowercase, 3))
        Select(row.find_element(*self.passenger_title)).select_by_visible_text('Mr')
        row.find_element(*self.passenger_first_name).clear()
        row.find_element(*self.passenger_first_name).send_keys('John')
        row.find_element(*self.passenger_last_name).clear()
        row.find_element(*self.passenger_last_name).send_keys(self.surname)

    # TODO: extend the functionality of this method to deal with children and infant passengers as well
    def fill_in_passenger_details(self, passengers):
        counter = 0
        passengers_rows = self.driver.find_elements(*self.passenger_rows)

        for i in range(passengers.get("adults", 1)):
            self._fill_in_older_passegers_details(passengers_rows[counter])
            counter += 1

        for i in range(passengers.get("teens", 0)):
            self._fill_in_older_passegers_details(passengers_rows[counter])
            counter += 1

        return self

    def fill_in_payment_details(self, card_number, card_type, expiry="12/2020", cvv="123"):
        # Debit/Credit card is selected by default
        self.element(self.card_number).clear()
        self.element(self.card_number).send_keys(card_number)
        Select(self.element(self.card_type)).select_by_visible_text(card_type)
        month, year = expiry.split('/')
        Select(self.element(self.card_expiry_month)).select_by_visible_text(month)
        Select(self.element(self.card_expiry_year)).select_by_visible_text(year)
        self.element(self.card_cvv).clear()
        self.element(self.card_cvv).send_keys(cvv)
        self.element(self.cardholder).clear()
        self.element(self.cardholder).send_keys('John Doe')
        self.element(self.address_line_1).clear()
        self.element(self.address_line_1).send_keys("21 Sun Lane")
        self.element(self.address_city).clear()
        self.element(self.address_city).send_keys("Cork")
        return self

    def submit(self):
        self.element(self.terms_tick).click()
        self.element(self.pay_now_btn).click()
        return self

    def is_error_shown(self):
        WebDriverWait(self.driver, 20).until(visibility_of_element_located(self.error_section))
        return self.element(self.error_section).is_displayed()
