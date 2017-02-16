from selenium import webdriver
from pages.flight_search_page import FlightSearchPage


def before_all(context):
    context.browser = webdriver.chrome.webdriver.WebDriver()
    context.browser.get('https://www.ryanair.com/ie/en/')
    # assuming we always start tests on the Flight Search page
    context.current_page = FlightSearchPage(context.browser)


def after_all(context):
    context.browser.quit()
