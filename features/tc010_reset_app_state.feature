Feature: Validate reset app state functionality

  Scenario: Reset application state after adding products to cart
    Given I am logged in as a standard user for reset app state
    And I have products added to the cart for reset
    When I open the menu and select Reset App State
    Then the cart should be empty
    And the application should be in its default state