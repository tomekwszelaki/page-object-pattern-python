from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.wait import WebDriverWait
from pages.flight_selection_page import FlightSelectionPage


class FlightSearchPage(object):
    def __init__(self, driver):
        self.driver = driver
        # store locators only. This way selenium will not try to search for these elements when instantiating
        # this class and avoid potential ELEMENT_NOT_FOUND exceptions in case of lazy loaded content
        self.one_way_flight_btn = (By.ID, 'flight-search-type-option-one-way')
        self.from_input = (By.CSS_SELECTOR, 'input[aria-labelledby="label-airport-selector-from"]')
        self.to_input = (By.CSS_SELECTOR, 'input[aria-labelledby="label-airport-selector-to"]')
        self.lets_go_btn = (By.CSS_SELECTOR, 'span[translate="common.buttons.lets_go"]')
        self.fly_out_field = 'div[name="startDate"]'
        self.fly_back_field = 'div[name="endDate"]'

        # Passenger selection popup
        self.passengers = (By.CSS_SELECTOR, 'div[name="passengers"]')
        self.passengers_adults = (By.CSS_SELECTOR, 'div[value="paxInput.adults"] button.inc')
        self.passengers_teens = (By.CSS_SELECTOR, 'div[value="paxInput.teens"] button.inc')
        self.passengers_children = (By.CSS_SELECTOR, 'div[value="paxInput.children"] button.inc')
        self.passengers_infants = (By.CSS_SELECTOR, 'div[value="paxInput.infants"] button.inc')

    def element(self, locator):
        # searching for the element each time we avoid the StaleElementReferenceException, but
        # communication with the selenium layer is the slowest part of the interaction so this
        # approach might be a performance issue.
        # TODO: once there are a few dozen tests run some performance analysis
        # TODO: this is a good candidate for a base class method
        return self.driver.find_element(*locator)

    def choose_a_one_way_flight(self):
        self.element(self.one_way_flight_btn).click()

    def set_departure(self, departure_from):
        from_input = self.element(self.from_input)
        from_input.clear()
        from_input.send_keys(departure_from)
        from_input.send_keys(Keys.ENTER)
        return self

    def set_destination(self, destination):
        to_input = self.element(self.to_input)
        to_input.clear()
        to_input.send_keys(destination)
        to_input.send_keys(Keys.ENTER)
        WebDriverWait(self.driver, 10).until(visibility_of_element_located((By.CSS_SELECTOR, self.fly_out_field)))
        return self

    def _set_date_helper(self, date, field):
        # TODO: automate clicking on the calendar popup - we might need a helper method that
        # will choose the closes day with a flight if there are no flight on the date provided

        # date fields consist of 3 separate inputs for the day, the month and the year
        dd, mm, yyyy = date.split('/')
        self.element((By.CSS_SELECTOR, field + ' .dd')).clear()
        self.element((By.CSS_SELECTOR, field + ' .dd')).send_keys(dd)
        self.element((By.CSS_SELECTOR, field + ' .mm')).clear()
        self.element((By.CSS_SELECTOR, field + ' .mm')).send_keys(mm)
        self.element((By.CSS_SELECTOR, field + ' .yyyy')).clear()
        self.element((By.CSS_SELECTOR, field + ' .yyyy')).send_keys(yyyy)
        return self

    def set_departure_date(self, departure_on):
        return self._set_date_helper(departure_on, self.fly_out_field)

    def set_return_date(self, return_on):
        return self._set_date_helper(return_on, self.fly_back_field)

    def _inc_passenger_count(self, passenger_type, how_many):
        for i in range(how_many):
            passenger_type.click()

    def add_passengers(self, adults=1, teens=0, children=0, infants=0):
        self.element(self.passengers).click()
        self._inc_passenger_count(self.element(self.passengers_adults), adults - 1)
        self._inc_passenger_count(self.element(self.passengers_teens), teens)
        self._inc_passenger_count(self.element(self.passengers_children), children)
        self._inc_passenger_count(self.element(self.passengers_infants), infants)

    def submit(self):
        self.element(self.lets_go_btn).click()
        return FlightSelectionPage(self.driver)
