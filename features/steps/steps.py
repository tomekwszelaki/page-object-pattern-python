from behave import given, when, then
from pyshould import should


@given('I make a booking from {_from} to {to} on {fly_out_date} for {adults} adults and {teens} teen')
def set_airports(context, _from, to, fly_out_date, adults, teens):
    context.passengers = {
        "adults": int(adults),
        "teens": int(teens)
    }

    context.current_page.choose_a_one_way_flight()
    context.current_page.set_departure(_from)
    context.current_page = context.current_page.set_destination(to)
    context.current_page.set_departure_date(fly_out_date)
    context.current_page.add_passengers(**context.passengers)
    context.current_page = context.current_page.submit()
    # calling submit on the FlightSearchPage has taken us to the FlightSelectionPage
    # let's wait until the next page is fully loaded before continuing
    context.current_page.is_ready()


@given('I choose fares that I like')
def set_fly_out_date(context):
    context.current_page.choose_outbound_flight()
    context.current_page = context.current_page.submit()
    # calling submit on the FlightSelectionPage has taken us to the FlightOptionsPage
    # let's wait until the next page is fully loaded before continuing
    context.current_page.is_ready()


@given('I don\'t select any add-ons')
def click_checkout_without_options(context):
    context.current_page = context.current_page.submit()
    # calling submit on the FlightOptionsPage has taken us to the FlightPaymentPage
    # let's wait until the next page is fully loaded before continuing
    context.current_page.is_ready()


@when('I pay for booking with card details {card_number} {card_type} {expiry}')
def set_billing_data(context, card_number, card_type, expiry):
    context.current_page.is_logged_in()
    context.current_page.fill_in_passenger_details(context.passengers)
    context.current_page.fill_in_payment_details(card_number, card_type)
    context.current_page.submit()


@then('I should get payment declined message')
def check_error_message(context):
    page = context.current_page
    page.is_error_shown() | should.be_true
    page.element(page.error_section_msg).text | should.begin_with("As your payment was not authorised we could not complete your reservation.")
