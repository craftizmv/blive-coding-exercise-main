@task1
Feature: Task 1

    The HTTP server should return 200 for the healthcheck endpoint

    Scenario: Healthcheck
        Given the server is running
        When I make an HTTP GET request to /healthcheck
        Then the response code should be 200
