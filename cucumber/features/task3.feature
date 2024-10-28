@task3
Feature: Task 3

  Scenario Outline: Channel Metadata Responses
    Given the server is running
    When I make an HTTP GET request to /v2/channels/<channel_id>
    Then the response code should be <status>
    And the response body should match fixtures/channels/<channel_id>/get_v2.json

    Examples:
      | channel_id   | status |
      | channelA     | 200    |
      | channelB     | 404    |
      | channelError | 500    |
