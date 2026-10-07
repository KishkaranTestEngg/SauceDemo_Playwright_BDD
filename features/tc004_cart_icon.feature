Feature: Cart icon visibility

  Scenario: Verify cart icon is visible after login
    Given I am logged in as "standard_user"
    When I am on the product listing page
    Then the cart icon should be visible