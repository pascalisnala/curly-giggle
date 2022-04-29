import os

TOKEN = os.getenv("TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")
PAGE_ID = os.getenv("PAGE_ID")
ENVIRONMENT = os.getenv("ENVIRONMENT")
HEADERS = {
    "Authorization": "Bearer " + TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16",
}
