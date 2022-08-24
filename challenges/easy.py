import pathlib
import sys

path = pathlib.Path(__file__).parent.resolve().parent.resolve()
sys.path.append(f"{path}/")

import json
from time import sleep
import requests

from videomatik.videomatik import Videomatik


def run_easy_challenge(email: str, api_key: str):
    print("Getting products...")

    products = (
        requests.get(f"https://videomatik.com.br/api/desafio-tdc?email={email}")
        .json()
        .get("products", [])
    )

    print(f"Products received: {len(products)}")

    print("*" * 20)

    queue = []

    videomatik = Videomatik(api_key=api_key)
    template_id = "oferta-varejo-nujyuua"

    print(f"Generating videos... - Template: {template_id}")

    for product in products:
        print("*" * 10)
        print(f"Generating for product: {product.get('name')}")

        custom_json = {
            "soundtrack": {"startTime": 0, "source": ""},
            "images": [
                {
                    "path": "assets[0]",
                    "source": "https://storage.videomatik.com.br/videomatik/templates/oferta-varejo-nujyuua/assets/oxdh6mre--compressed-png.png",
                },
                {"path": "assets[1]", "source": product.get("image")},
            ],
            "version": "1",
            "texts": [
                {
                    "fillColor": "#ffffff",
                    "fontStyle": "Bold",
                    "path": "assets[3].layers[0].t.d.k[0]",
                    "fontWeight": "700",
                    "fontAscent": 71.5988159179688,
                    "hidden": None,
                    "time": 0,
                    "fontSize": 53,
                    "value": "",
                    "justification": "CENTER",
                    "fontFamily": "Arial",
                    "stroke": None,
                    "fontName": "Arial-BoldMT",
                    "lineHeight": 63.6,
                },
                {
                    "fillColor": "#ffffff",
                    "fontStyle": "Bold",
                    "path": "assets[3].layers[1].t.d.k[0]",
                    "fontWeight": "700",
                    "fontAscent": 71.5988159179688,
                    "hidden": None,
                    "time": 0,
                    "fontSize": 129,
                    "value": product.get("price"),
                    "justification": "CENTER",
                    "fontFamily": "Arial",
                    "stroke": None,
                    "fontName": "Arial-BoldMT",
                    "lineHeight": 154.8,
                },
                {
                    "fillColor": "#000000",
                    "fontStyle": "Bold",
                    "path": "assets[3].layers[3].t.d.k[0]",
                    "fontWeight": "700",
                    "fontAscent": 71.5988159179688,
                    "hidden": None,
                    "time": 0,
                    "fontSize": 31,
                    "value": product.get("description"),
                    "justification": "CENTER",
                    "fontFamily": "Arial",
                    "stroke": None,
                    "fontName": "Arial-BoldMT",
                    "lineHeight": 39,
                },
                {
                    "fillColor": "#000000",
                    "fontStyle": "Bold",
                    "path": "assets[3].layers[5].t.d.k[0]",
                    "fontWeight": "700",
                    "fontAscent": 71.5988159179688,
                    "hidden": None,
                    "time": 0,
                    "fontSize": 88,
                    "value": product.get("name"),
                    "justification": "CENTER",
                    "fontFamily": "Arial",
                    "stroke": None,
                    "fontName": "Arial-BoldMT",
                    "lineHeight": 98,
                },
                {
                    "fillColor": "#ffffff",
                    "fontStyle": "Bold",
                    "path": "assets[4].layers[2].t.d.k[0]",
                    "fontWeight": "700",
                    "fontAscent": 71.5988159179688,
                    "hidden": None,
                    "time": 0,
                    "fontSize": 134,
                    "value": "APROVEITE\nAS OFERTAS",
                    "justification": "CENTER",
                    "fontFamily": "Arial",
                    "stroke": None,
                    "fontName": "Arial-BoldMT",
                    "lineHeight": 151,
                },
            ],
            "shapes": [
                {"path": "assets[2].layers[2].shapes[0].it[2]", "color": "#aa1e0d"},
                {"path": "assets[3].layers[2].shapes[0].it[2]", "color": "#aa1e0d"},
                {"path": "assets[3].layers[9].shapes[0].it[2]", "color": "#aa1e0d"},
                {"path": "assets[3].layers[10].shapes[0].it[1]", "color": "#ffffff"},
                {"path": "assets[3].layers[10].shapes[0].it[2]", "color": "#ffffff"},
                {"path": "assets[4].layers[3].shapes[0].it[2]", "color": "#aa1e0d"},
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

    with open("export/easy.json", "w") as ex_file:
        ex_file.write(json.dumps(results, indent=2))


run_easy_challenge("<email>", "<chave_api>")
