import json

from behave import given, when, then, step
from hamcrest import assert_that, equal_to


@given("the server is running")
def step_impl(context):
    assert_that(context.jobs_api.is_running(), equal_to(True))


@when("I make an HTTP GET request to {path}")
def step_impl(context, path):
    context.resp = context.jobs_api.get(path)


@then("the response code should be {code}")
def step_impl(context, code):
    assert_that(context.resp.status_code, equal_to(int(code)))


@step("the response body should match {fixture}")
def step_impl(context, fixture):
    with open(fixture, 'r') as f:
        expected = json.load(f)
    assert_that(context.resp.json(), equal_to(expected))
