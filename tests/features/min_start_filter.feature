Feature: --min-start filter

  As a user,
  I want to filter meetings that are too early,
  So that I can reduce the search space and review fewer solutions.

  Scenario: Filter out meetings that are too early
    Given a doodle poll with 24 meetings one per hour
    When I specify --min-start=<threshold>
    Then I should see <filtered> meetings were filterd.

    Examples:
    | threshold | filtered |
    |    4      |    4     |
    |    13     |    13    |
    |    0      |    0     |
    |    24     |    24    |
