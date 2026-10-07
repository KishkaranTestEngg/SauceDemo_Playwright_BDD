Feature: Add selected products to cart

  Scenario: Add 4 randomly selected products to cart and validate cart count
    Given I am logged in as "standard_user"
    When I randomly select 4 products and add them to the cart
    Then the cart icon should show a count of 4
    And the 4 selected products should be listed in the cart