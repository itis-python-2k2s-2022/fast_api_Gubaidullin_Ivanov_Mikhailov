import json
import requests


def get_atms():
    data = {
        "bounds": {
            "bottomLeft": {
                "lat": 55.77299229960861,
                "lng": 48.95159280821545
            },
            "topRight": {
                "lat": 55.8228887639529,
                "lng": 49.367699985949834
            }
        },
        "filters": {
            "banks": [
                "tcs"
            ],
            "showUnavailable": False,
            "currencies": [
                "USD"
            ]
        },
        "zoom": 12
    }

    response = json.loads(requests.post("https://api.tinkoff.ru/geo/withdraw/clusters", json=data).content.decode())
    points = {"points": []}

    for cluster in response["payload"]["clusters"]:
        for point in cluster["points"]:
            element = {
                "id": point["id"],
                "location": point["location"],
            }
            points["points"].append(element)

    return points


def compare_dicts(dict_new: dict, dict_old: dict):
    changes = {}
    found = False
    for element_new in dict_new["points"]:
        for element_old in dict_old["points"]:
            if element_new["id"] == element_old["id"]:
                found = True
                break

        if not found:
            found = False
            try:
                changes["added"].append(element_new["id"])
            except KeyError:
                changes["added"] = []
                changes["added"].append(element_new["id"])
    found = False

    for element_old in dict_old["points"]:
        for element_new in dict_new["points"]:
            if element_new["id"] == element_old["id"]:
                found = True
                break

        if not found:
            found = False
            try:
                changes["removed"].append(element_old["id"])
            except KeyError:
                changes["removed"] = []
                changes["removed"].append(element_old["id"])

    return changes
