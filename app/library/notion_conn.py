import requests
import datetime
import re
import time
import asyncio
import aiohttp


from .notion2html import article_content, article_title, insert_toggle_content
from . import config as cfg


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
        if obj["properties"][cfg.ENVIRONMENT]["checkbox"]:
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

            out[title]["domain"] = obj["properties"]["Domain Knowledge"]["select"][
                "name"
            ]
            out[title]["tags"] = [
                tag["name"] for tag in obj["properties"]["Tags"]["multi_select"]
            ]
            out[title]["url"] = re.findall(r"\/[\w-]+$", obj["url"])[0][1:].lower()
            out[title]["page_id"] = re.findall(r"-\w+$", obj["url"])[0][1:]

    return out


async def get_article_metadata(id, headers):
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


async def process_block(block, id=None, headers=None):
    if block["type"] == "toggle":
        contents = "".join(await get_article_content(id, headers))
        return await article_content(block) + await insert_toggle_content(contents)
    else:
        return await article_content(block)


async def get_article_content(id, headers):
    tasks = []
    url = f"https://api.notion.com/v1/blocks/{id}/children"
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers, ssl=False) as res:
            data = await res.json()
    contents = data["results"]
    for block in contents:
        tasks.append(asyncio.create_task(process_block(block, block["id"], headers)))
    responses = await asyncio.gather(*tasks)
    return responses


async def get_article(id, headers):
    tasks = []
    tasks.append(asyncio.create_task(get_article_metadata(id, headers)))
    tasks.append(asyncio.create_task(get_article_content(id, headers)))
    responses = await asyncio.gather(*tasks)
    cover, title = responses[0]
    content = responses[1]
    content = "".join(content)
    return cover, title + content
