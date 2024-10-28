from features.support.jobs_api import JobsApi
from features.support.blive_api_mock import BliveApiMock



def before_all(context):
    context.jobs_api = JobsApi()
    context.jobs_api.start()

    context.blive_api = BliveApiMock()
    context.blive_api.start()

def after_all(context):
    context.jobs_api.stop()
    context.blive_api.stop()