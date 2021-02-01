Feature: Test Feature 3
  # Enter feature description here

  @example
  Scenario: Validate parallel run of scenario1 from feature3
    Given I have a scenario setup that takes between 1 and 10 seconds
    Then I print the time it took for this setup

  @example
  Scenario: Validate parallel run of scenario2 from feature3
    Given I have a scenario setup that takes between 5 and 10 seconds
    Then I print the time it took for this setup

  @skip
  Scenario: Validate parallel run of scenario3 from feature3
    Given I have a scenario setup that takes between 10 and 20 seconds
    Then I print the time it took for this setup