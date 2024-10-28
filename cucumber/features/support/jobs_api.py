import json
import os
import subprocess
from multiprocessing import Process, set_start_method
from typing import Optional

import requests


class JobsApi:

    def __init__(self):
        self.endpoint = None
        self._is_running = False
        self.app: Optional[Process] = None

    def start(self):
        if os.getenv("NO_UNDERTEST") is None:
            set_start_method('spawn')
            env = os.environ.copy()
            env['CONFIG_URL'] = './app_config.json'
            env['AWS_ACCESS_KEY_ID'] = 'foo'
            env['AWS_SECRET_ACCESS_KEY'] = 'bar'
            with open('./logs/app.log', 'w') as out:
                self.app = subprocess.Popen(
                    ['../bin/app.test', '-test.run', '^TestRunMain$',
                     '-test.coverprofile=./coverage/int-cover.profile'],
                    env=env,
                    stdout=out,
                    stderr=out
                )
                self._is_running = True

        with open('./app_config.json', 'r') as cfg_file:
            cfg = json.load(cfg_file)
            self.endpoint = f"http://localhost{cfg['internal_http_address']}"
        self._poll_ready()

    def stop(self):
        if self.app is not None:
            self.app.terminate()
            self.app.wait()

    def _poll_ready(self):
        print("polling server")
        started = False
        while not started:
            try:
                resp = requests.get(f"{self.endpoint}/healthcheck")
                if resp.status_code == 200:
                    started = True
                    break
            except requests.exceptions.RequestException:
                pass

        print("app started")

    def post(self, path, body, headers=None) -> requests.Response:
        if headers is None:
            headers = {}
        return requests.post(f"{self.endpoint}{path}", body, headers=headers)

    def get(self, path, headers=None) -> requests.Response:
        if headers is None:
            headers = {}
        return requests.get(f"{self.endpoint}{path}", headers=headers)

    def put(self, path, body, headers=None) -> requests.Response:
        if headers is None:
            headers = {}
        return requests.put(f"{self.endpoint}{path}", body, headers=headers)

    def delete(self, path, headers=None) -> requests.Response:
        if headers is None:
            headers = {}
        return requests.delete(f"{self.endpoint}{path}", headers=headers)

    def is_running(self) -> bool:
        return self._is_running
