from multiprocessing.sharedctypes import Value
import get_wallet
import requests
import datetime
from requests import get
from datetime import datetime
import time
import telegram_send
import pandas

ETHERSCAN_KEY = '42T1XZPXVCNZDDW6DW2AAA1TNZ853U91VP'
BASE_URL = "https://api.etherscan.io/api"
ETHER_VALUE = 10 ** 18

BOT_TOKEN = '5333598588:AAHRUbuRuCvzh4aALDuIi8JTPYPCShGd_L0'

name = ['whale #1', 'whale #2', 'whale #3']
wallet_list = get_wallet.get_address()
whale_address = dict(zip(name, wallet_list))

t_time = {}
amount = {}

for key in whale_address:
    t_time[key] = 0
    amount[key] = 0

check_again = True

def create_api_url(module, action, address, **kwargs):
	url = BASE_URL + f"?module={module}&action={action}&address={address}&apikey={ETHERSCAN_KEY}"

	for key, value in kwargs.items():
		url += f"&{key}={value}"

	return url

def format_tx(tx: dict) -> str:
    return f'From: {tx["from"]}, To: {tx["to"]}, Amount: {int(tx["value"]) / ETHER_VALUE}'


while True:
    time.sleep(1)
    while check_again:
        for whale in whale_address:
            transactions_url = create_api_url("account", "txlist", whale_address[whale], startblock=0, endblock=99999999, page=1, offset=10000, sort="asc")
            response = get(transactions_url)
            df = pandas.read_json(transactions_url)
            data = df['result']

            recent_time = data[0][int(tx['timeStamp'])]
            recent_amount = data[0][int(tx['value'])]

            if recent_time != t_time[whale]:
                t_time[whale] = recent_time
                amount[whale] = recent_amount

                if int(recent_amount) > 0:
                    port = '🔒 🔒 🔒 🔒 🔒 🔒 🔒 holding'
                elif int(recent_amount) < 0:
                    port = '🚨 🚨 🚨 🚨 🚨 🚨 🚨 dumping'
                
                amount_in_eth = int(recent_amount) / ETHER_VALUE
                telegram_send.send(messages=[f'New transactions occured for {whale} !'])
                telegram_send.send(messages=[f'Whale Alert: {whale} is {port} {amount_in_eth} ETH'])
                telegram_send.send(messages=[format_tx(data[0])])
            time.sleep(15)

        check_again = False
    
    now      = datetime.datetime.now(datetime.timezone.utc)
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    minutes  = ((now - midnight).seconds) // 60

    if (minutes % 60) == 0:
        telegram_send.send(messages=['Whale monitoring bot is working 🤖🤖🤖'])    
        time.sleep(60)
        check_again = True

                    