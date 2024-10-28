@task2
Feature: Task 2

    Scenario Outline: Channel Metadata Responses
        Given the server is running
        When I make an HTTP GET request to /v1/channels/<channel_id>
        Then the response code should be <status>
        And the response body should match fixtures/channels/<channel_id>/get.json

        Examples:
            | channel_id | status |
            | channelA   | 200    |
            | channelB   | 404    |
