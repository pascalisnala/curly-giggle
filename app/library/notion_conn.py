import requests
import datetime
import re

from .notion2html import article_content, article_title


def get_all_domains(id, headers):
    url = f"https://api.notion.com/v1/databases/{id}"

    res = requests.request("GET", url, headers=headers)
    data = res.json()

    domains = {
        domain["name"]: domain["color"]
        for domain in data["properties"]["Domain Knowledge"]["select"]["options"]
    }
    return domains


def get_article_list(id, headers, domain=None, k=None):
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
        ).strftime("%b %d, %Y")
        out[title]["last_edited_date"] = datetime.datetime.strptime(
            obj["last_edited_time"], "%Y-%m-%dT%H:%M:%S.%fZ"
        ).strftime("%b %d, %Y")

        out[title]["domain"] = obj["properties"]["Domain Knowledge"]["select"]["name"]
        out[title]["tags"] = [
            tag["name"] for tag in obj["properties"]["Tags"]["multi_select"]
        ]
        out[title]["url"] = re.findall(r"\/[\w-]+$", obj["url"])[0][1:].lower()
        out[title]["page_id"] = re.findall(r"-\w+$", obj["url"])[0][1:]

    return out


def get_article_metadata(id, headers):
    # metadata
    url = f"https://api.notion.com/v1/pages/{id}"
    res = requests.request("GET", url, headers=headers)
    data = res.json()
    out = {}
    out["title"] = data["properties"]["Title"]["title"][0]["plain_text"]
    if data["cover"] != None:
        out["cover_url"] = data["cover"]["external"]["url"]
    else:
        out["cover_url"] = None
    out["author"] = "Nala Krisnanda"
    out["domain"] = data["properties"]["Domain Knowledge"]["select"]["name"]
    out["domain_color"] = data["properties"]["Domain Knowledge"]["select"]["color"]
    out["created_time"] = datetime.datetime.strptime(
        data["created_time"], "%Y-%m-%dT%H:%M:%S.%fZ"
    ).strftime("%b %d, %Y")
    out["tags"] = [tag["name"] for tag in data["properties"]["Tags"]["multi_select"]]

    return article_title(out)


def get_article_content(id, headers):
    # content
    url = f"https://api.notion.com/v1/blocks/{id}/children"
    res = requests.request("GET", url, headers=headers)
    data = res.json()
    return article_content(data["results"])


def get_article(id, headers):
    cover, title = get_article_metadata(id, headers)
    content = get_article_content(id, headers)
    return cover, title + content
