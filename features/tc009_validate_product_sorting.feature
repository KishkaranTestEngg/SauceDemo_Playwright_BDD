Feature: Validate product sorting functionality

  Scenario: Sort products by price low to high
    Given I am logged in as a standard user for sorting
    When I select "Price (low to high)" from the sort dropdown
    Then the products should be displayed in ascending price order

  Scenario: Sort products by name Z to A
    Given I am logged in as a standard user for sorting
    When I select "Name (Z to A)" from the sort dropdown
    Then the products should be displayed in descending name order