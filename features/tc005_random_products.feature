Feature: Random product selection and data extraction

  Scenario: Randomly select 4 products and fetch their names and prices
    Given I am logged in as "standard_user"
    When I randomly select 4 products from the product listing
    Then the selected product names and prices should be displayed correctly