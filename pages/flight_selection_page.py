from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from pages.flight_options_page import FlightOptionsPage


class FlightSelectionPage(object):
    def __init__(self, driver):
        self.driver = driver
        self.promotional_popup_btn = (By.CSS_SELECTOR, '.modal-dialog button.core-btn-primary')
        # this selector is ambiguous, there might be multiple elements that match this selector if there are
        # many outbound/inbound flights. When that happens, this selector will simply return the first element
        # TODO: implement a proper way of selecting a flight
        self.outboud_flights = {
            "list": (By.CSS_SELECTOR, 'flights-table[type="outbound"] .flights-table .flight-header'),
            "fare": (By.CSS_SELECTOR, 'flights-table[type="outbound"] .flights-table-fares .standard button')
        }
        self.return_flights = {
            "list": (By.CSS_SELECTOR, 'flights-table[type="inbound"] .flights-table .flight-header'),
            "fare": (By.CSS_SELECTOR, 'flights-table[type="inbound"] .flights-table-fares .standard button')
        }
        self.continue_btn = (By.CSS_SELECTOR, '.flight-selector__listing-footer-button-next')
        print('FlightSelectionPage instantiated')

    def deal_with_popups(self):
        try:
            popup_btn = self.element(self.promotional_popup_btn)
        except NoSuchElementException as e:
            # modal was not show, so we're good to go
            pass
        else:
            popup_btn.click()
            WebDriverWait(self.driver, 5).until(staleness_of(popup_btn))

    def is_ready(self):
        WebDriverWait(self.driver, 20).until(visibility_of_element_located(self.outboud_flights["list"]))
        self.deal_with_popups()

    def element(self, locator):
        return self.driver.find_element(*locator)

    def _choose_a_flight(self, choose_from):
        self.element(choose_from["list"]).click()
        WebDriverWait(self.driver, 10).until(element_to_be_clickable(choose_from["fare"])).click()
        return self

    def choose_outbound_flight(self):
        return self._choose_a_flight(self.outboud_flights)

    def choose_return_flight(self):
        return self._choose_a_flight(self.return_flights)

    def submit(self):
        WebDriverWait(self.driver, 10).until(element_to_be_clickable(self.continue_btn)).click()
        return FlightOptionsPage(self.driver)
