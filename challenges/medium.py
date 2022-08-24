import pathlib
import sys

path = pathlib.Path(__file__).parent.resolve().parent.resolve()
sys.path.append(f"{path}/")

import json
from time import sleep
import requests

from videomatik.videomatik import Videomatik


def run_medium_challenge(api_key: str):
    print("Getting people...")

    people = (
        requests.get(f"https://swapi.dev/api/people?limit=1").json().get("results", [])
    )

    print(f"People received: {len(people)}")

    print("*" * 20)

    queue = []

    videomatik = Videomatik(api_key=api_key)
    template_id = "podcast-5obo1to"

    print(f"Generating videos... - Template: {template_id}")

    for person in people:
        print("*" * 10)
        print(f"Generating for person: {person.get('name')}")

        custom_json = {
            "soundtrack": {"startTime": 0, "source": ""},
            "images": [
                {
                    "path": "assets[0]",
                    "source": "https://storage.videomatik.com.br/videomatik/templates/podcast-5obo1to/assets/mbijerxm--compressed-jpg.jpg",
                }
            ],
            "version": "1",
            "texts": [
                {
                    "fillColor": "#767676",
                    "fontStyle": "Medium",
                    "path": "layers[0].t.d.k[0]",
                    "fontWeight": "",
                    "fontAscent": 74.1989135742188,
                    "hidden": None,
                    "time": 0,
                    "fontSize": 55,
                    "value": f'\n{person.get("gender")} - {person.get("height")}cm - {person.get("mass")}kg',
                    "justification": "CENTER",
                    "fontFamily": "Montserrat",
                    "stroke": None,
                    "fontName": "Montserrat-Medium",
                    "lineHeight": 66,
                },
                {
                    "fillColor": "#1e212b",
                    "fontStyle": "Bold",
                    "path": "layers[1].t.d.k[0]",
                    "fontWeight": "700",
                    "fontAscent": 74.1989135742188,
                    "hidden": None,
                    "time": 0,
                    "fontSize": 53,
                    "value": person.get("name"),
                    "justification": "CENTER",
                    "fontFamily": "Montserrat",
                    "stroke": None,
                    "fontName": "Montserrat-Bold",
                    "lineHeight": 63.599999999999994,
                },
            ],
            "shapes": [
                {
                    "path": "assets[1].layers[2].shapes[0].it[2].it[1]",
                    "color": "#561515",
                },
                {
                    "path": "assets[1].layers[3].shapes[0].it[2].it[1]",
                    "color": "#561515",
                },
                {"path": "layers[3].shapes[0].it[1]", "color": "#ffffff"},
                {"path": "layers[5].shapes[0].it[1]", "color": "#ffffff"},
                {"path": "layers[6].shapes[0].it[1]", "color": "#2c3e50"},
            ],
        }

        video_req = videomatik.create_video_request(
            template_id=template_id, custom_json=custom_json
        )

        print(f"Requested - {video_req.status_code}")

        if video_req.status_code == 200:
            data = video_req.json()
            print(f'Request id: {data.get("id")}')
            queue.append(data)
        else:
            print(video_req.text)

    print("*" * 20)

    sleep(1)

    results = []

    print(f"Checking results...")

    try:
        while len(queue) > 0:
            print("*" * 10)

            item = queue.pop(0)
            print(f"Request: {item.get('id')}")

            try:
                video_req = videomatik.get_video_request(
                    request_id=item.get("id", None)
                )
                data = video_req.json()
            except Exception as exc:
                print("Error", exc)
                queue.append(item)
                continue

            print(f'State: {data.get("renderJob", {}).get("state")}')

            if data.get("renderJob", {}).get("state", "error") in ["finished", "error"]:
                results.append(data)
            else:
                queue.append(item)

            sleep(0.25)

    except KeyboardInterrupt:
        pass

    with open("export/medium.json", "w") as ex_file:
        ex_file.write(json.dumps(results, indent=2))


run_medium_challenge("<chave_api>")
