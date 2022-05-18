from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
import json

group_id = "@zkSyncc"
api_id = 10956225
api_hash = '78f50dacad7c81fbe9c7f14baf73f9fc'
accounts = []


def get_accounts():
    f = open('accounts.json')
    account = json.load(f)
    global api_id
    global api_hash
    api_id = account["api_id"]
    api_hash = account["api_hash"]
    global accounts
    accounts = account["accounts"]


get_accounts()

for account in accounts:
    with TelegramClient(account, api_id, api_hash) as client:
        client.loop.run_until_complete(client(JoinChannelRequest(group_id)))
        print("{} connected!".format(account))
