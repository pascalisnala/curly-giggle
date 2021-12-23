import requests
import datetime

token = "secret_RIXZJ45mgLxYHHXeIQFXJaX4cobAL6OCo6Va3yFvZUb"

database_id = "46f0183f4ca64e9b8e9d2b53917bdef1"
page_id = "692ec7c9f027439fa2c0985a5c17f764"

headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16",
}


def get_domains(id, headers):
    url = f"https://api.notion.com/v1/databases/{id}"

    res = requests.request("GET", url, headers=headers)
    data = res.json()

    domains = [
        domain["name"]
        for domain in data["properties"]["Domain Knowledge"]["select"]["options"]
    ]

    print(domains)


def get_articles_metadata(id, headers, domain=None):
    url = f"https://api.notion.com/v1/databases/{id}/query"

    if domain:
        filter = (
            """
        {"filter": {"property": "Domain Knowledge", "select":{"equals":"%s"}},
        "sorts": [{"timestamp": "created_time", "direction": "descending"}]
        }
        """
            % domain
        )
    else:
        filter = ""

    res = requests.request("POST", url, headers=headers, data=filter)
    data = res.json()

    out = {}

    for obj in data["results"]:
        title = obj["properties"]["Title"]["title"][0]["plain_text"]
        out[title] = {}
        out[title]["created_time"] = datetime.datetime.strptime(
            obj["created_time"], "%Y-%m-%dT%H:%M:%S.%fZ"
        ).strftime("%Y-%m-%d %H:%M:%S")
        out[title]["last_edited_time"] = datetime.datetime.strptime(
            obj["last_edited_time"], "%Y-%m-%dT%H:%M:%S.%fZ"
        ).strftime("%Y-%m-%d %H:%M:%S")

        out[title]["created_date"] = datetime.datetime.strptime(
            obj["created_time"], "%Y-%m-%dT%H:%M:%S.%fZ"
        ).strftime("%Y-%m-%d")
        out[title]["last_edited_date"] = datetime.datetime.strptime(
            obj["last_edited_time"], "%Y-%m-%dT%H:%M:%S.%fZ"
        ).strftime("%Y-%m-%d")

        out[title]["domain"] = obj["properties"]["Domain Knowledge"]["select"]["name"]
        out[title]["tags"] = [
            tag["name"] for tag in obj["properties"]["Tags"]["multi_select"]
        ]
        out[title]["link2full"] = obj["url"]

    return out


def read_page(id, headers):
    readUrl = f"https://api.notion.com/v1/pages/{id}"

    res = requests.request("GET", readUrl, headers=headers)
    data = res.json()
    print(res.status_code)


def read_block(id, headers):
    readUrl = f"https://api.notion.com/v1/blocks/{id}/children"

    res = requests.request("GET", readUrl, headers=headers)
    data = res.json()
    print(res.status_code)


def read_page(id, headers):
    readUrl = f""


# read_block(page_id, headers)
# read_page(page_id, headers)
# read_database(database_id, headers)

# get_domains(database_id, headers)
import sys

print(sys.prefix)
print(get_articles_metadata(database_id, headers))
