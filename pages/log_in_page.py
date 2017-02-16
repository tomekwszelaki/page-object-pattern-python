from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait
from os import environ


class LogInPage(object):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.email_field = (By.CSS_SELECTOR, 'div[ng-switch-when="login"] input[name="emailAddress"')
        self.password_field = (By.CSS_SELECTOR, 'div[ng-switch-when="login"] input[name="password"')
        self.remember_me_tick = (By.CSS_SELECTOR, 'div[ng-switch-when="login"] input[name="remember"')
        self.log_in_btn = (By.CSS_SELECTOR, 'div[ng-switch-when="login"] button[type="submit"]')

    def is_ready(self):
        self.wait.until(element_to_be_clickable(self.log_in_btn))

    def element(self, locator):
        return self.driver.find_element(*locator)

    def log_in(self, email, password=None, remember_me=True):
        password = password if password is not None else environ.get('RYANAIR_PASS_' + email.upper())
        email_field = self.element(self.email_field)

        email_field.clear()
        email_field.send_keys(email)
        self.element(self.password_field).clear()
        self.element(self.password_field).send_keys(password)

        if not remember_me:
            self.element(self.remember_me_tick).click()

            self.element(self.log_in_btn).click()
            # wait until the log in form disappears
            self.wait.until(staleness_of(email_field))
