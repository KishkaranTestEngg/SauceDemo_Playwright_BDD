Feature: Complete checkout and validate order

  Scenario: Complete checkout and verify order confirmation
    Given I am logged in as a standard user for checkout
    And I have a product added to the cart for checkout
    When I proceed to checkout
    And I enter the checkout user details
    Then I should see the order summary
    And the order summary should contain the correct product
    And I capture the order summary screenshot
    When I finalize the order
    Then I should see the order confirmation message
