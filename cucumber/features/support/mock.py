from threading import Thread

import bottle
import requests


class MockApi(bottle.Bottle):

    def __init__(self, addr, port):
        super(MockApi, self).__init__()
        self.thread = None
        self.addr = addr
        self.port = port
        self.route("/v1/probes/ready", callback=self.probe)

    @staticmethod
    def probe():
        return "letsrockandroll"

    def start(self):
        self.thread = Thread(target=lambda: self.run(port=self.port, host=self.addr), daemon=True)
        print(f"Starting mock at {self.port}")
        self.thread.start()
        self._poll_ready()

    def _poll_ready(self):
        started = False
        while not started:
            try:
                resp = requests.get(f"http://{self.addr}:{self.port}/v1/probes/ready")
                if resp.status_code == 200:
                    started = True
                    break
            except requests.exceptions.RequestException:
                pass

        print(f"mock started at {self.port}")

    @staticmethod
    def stop():
        # TODO: thread.stop won't stop the thread. There is no method called stop on thread
        # since bottle is demonized it's probably ok to not stop them explicitly and let them
        # die on cuke end
        print("Stopping mock")
