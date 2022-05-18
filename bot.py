from telethon import TelegramClient
import json
import random
import time
import asyncio
import codecs
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

class Group:
    def __init__(self, group_id):
        self.group_id = group_id


api_id = 10956225
api_hash = '78f50dacad7c81fbe9c7f14baf73f9fc'
messages = []
accounts = []
user_list = []
message_count = 0
account_count = 0

clients = []

groups = []


def get_groups():
    f = open('groups.json')
    data = json.load(f)
    global groups
    json_groups = data["accounts"]
    for json_group in json_groups:
        group_id = json_group["groupID"]
        group = Group(group_id)
        global groups
        groups.append(group)


def get_messages():
    message_file = codecs.open("messages.txt", "r", "utf_8_sig")
    global messages
    message = message_file.read()
    messages.append(message)
    global message_count
    message_count = len(messages)


def get_accounts():
    f = open('accounts.json')
    account = json.load(f)
    global api_id
    global api_hash
    api_id = account["api_id"]
    api_hash = account["api_hash"]
    global accounts
    accounts = account["accounts"]
    global account_count
    account_count = len(accounts)


get_messages()
get_accounts()
get_groups()

loop_condition = True

message = messages[0]
for group in groups:
    offset = 0
    limit = account_count - 1
    while loop_condition:
        if account_count < 2:
            exit(1)
        first_account = accounts[0]
        with TelegramClient(first_account, api_id, api_hash) as client:
            participants = client.loop.run_until_complete(client(GetParticipantsRequest(
                group.group_id, ChannelParticipantsSearch(''), offset, limit,
                hash=0
            )))
        users = participants.users
        if len(users) < limit:
            loop_condition = False
        for index, user in enumerate(users):
            try:
                username = user.username
                if not username:
                    continue
                user_id = "@" + username
                account = accounts[index + 1]
                with TelegramClient(account, api_id, api_hash) as client:
                    client.loop.run_until_complete(client.send_message(user_id, message))
                    print("sent message to :", user_id)
                    print("sleeping 60 seconds.")
                    time.sleep(60)
            except:
                pass
        offset += limit
    offset += limit
