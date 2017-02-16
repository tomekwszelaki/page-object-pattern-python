Feature: Unsuccessful booking
  As a freelance SDET
  I would like to automate the unsuccessful booking scenario
  So that I can land a job with Travel Labs :)

  Scenario Outline: Should decline a booking when the card number is incorrect
    Given I make a booking from DUB to SXF on 11/03/2017 for 2 adults and 1 teen
    And I choose fares that I like
    And I don't select any add-ons
    When I pay for booking with card details <card_number> <card_type> <expiry>
    Then I should get payment declined message

    Examples:
    | card_number           | card_type   | expiry  |
    | 5555555555555557      | MasterCard  | 10/18   |
