Feature: Validate product details inside the cart

  Scenario: Validate added product details in the cart
    Given I am logged in as "standard_user"
    When I randomly select 4 products and add them to the cart
    And I navigate to the cart page
    Then the cart product details should match the selected products