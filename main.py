import requests
import json

token = 'secret_RIXZJ45mgLxYHHXeIQFXJaX4cobAL6OCo6Va3yFvZUb'

database_id = '46f0183f4ca64e9b8e9d2b53917bdef1'
page_id = '692ec7c9-f027-439f-a2c0-985a5c17f764'

headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16"
}

def dump_json(res, dir):
    with open(dir, 'w', encoding='utf8') as f:
        json.dump(res, f, ensure_ascii=False)

def read_database(id, headers):
    readUrl = f"https://api.notion.com/v1/databases/{id}/query"

    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    print(res.status_code)

    dump_json(data, "./json-dump/database_json.json")

def read_page(id, headers):
    readUrl = f"https://api.notion.com/v1/pages/{id}"

    res = requests.request("GET", readUrl, headers=headers)
    data = res.json()
    print(res.status_code)

    dump_json(data, "./json-dump/page_json.json")

def read_block(id, headers):
    readUrl = f"https://api.notion.com/v1/blocks/{id}/children"

    res = requests.request("GET", readUrl, headers=headers)
    data = res.json()
    print(res.status_code)

    dump_json(data, "./json-dump/block_json.json")


read_block(page_id, headers)
# read_page(page_id, headers)
# read_database(database_id, headers)
