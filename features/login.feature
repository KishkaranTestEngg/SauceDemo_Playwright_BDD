Feature: SauceDemo login with predefined users

  Scenario Outline: Login with different predefined users
    Given I am on the SauceDemo login page
    When I login with username "<username>" and password "secret_sauce"
    Then I should see the expected login behavior "<expected_behavior>"

    Examples:
      | username                | expected_behavior |
      | standard_user           | successful_login  |
      | performance_glitch_user | successful_login  |
      | locked_out_user         | locked_out        |
      | problem_user            | successful_login  |
      | error_user              | successful_login  |
      | visual_user             | successful_login  |

  Scenario: Login with invalid credentials
    Given I am on the SauceDemo login page
    When I login with username "invalid_user" and password "invalid_password"
    Then access should be denied

  Scenario: Validate logout functionality
    Given I am on the SauceDemo login page
    When I login with username "standard_user" and password "secret_sauce"
    Then I should be logged in successfully
    When I click the Logout button
    Then I should be redirected to the login screen