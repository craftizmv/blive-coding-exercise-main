import json

import bottle
from features.support.mock import MockApi


class BliveApiMock(MockApi):
    def __init__(self):
        super().__init__("127.0.0.1", 8081)
        self.get("/v2/ingest_point/<channel_id>", callback=self.ingest_url_callback)
        self.get("/v2/playback_point/<channel_id>", callback=self.playback_url_callback)

    @staticmethod
    def playback_url_callback(channel_id):
        if channel_id == "channelError":
            return bottle.HTTPResponse(status=500, body=json.dumps({"error_code": "error getting channel playback url"}))
        return {
            "playback_point": f"http://playback.{channel_id}.com/v2/{channel_id}",
        }

    @staticmethod
    def ingest_url_callback(channel_id):
        return {
            "ingest_point": f"rtmp://ingest.{channel_id}.com/v2/{channel_id}",
        }
