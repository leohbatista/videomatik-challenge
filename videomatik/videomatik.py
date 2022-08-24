import requests


class Videomatik:
    API_URL = "https://api.videomatik.com.br"
    API_KEY = None

    def __init__(self, api_key: str) -> None:
        self.API_KEY = api_key

    def create_video_request(
        self, template_id: str, custom_json: dict, composition_id: str = "default"
    ):
        payload = {
            "templateId": template_id,
            "compositionId": composition_id,
            "customJSON": custom_json,
            "actions": [],
        }

        headers = {"Authorization": self.API_KEY, "Content-Type": "application/json"}

        return requests.post(
            f"{self.API_URL}/v1/video-requests", headers=headers, json=payload
        )

    def get_video_request(self, request_id: str = None):
        headers = {"Authorization": self.API_KEY}

        return requests.get(
            f"{self.API_URL}/v1/video-requests/{request_id}", headers=headers
        )
