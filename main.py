import sys
import asyncio
import aiohttp
from time import time
from pprint import pprint as print
from datetime import datetime, timedelta

async def main(user_input):
    corrutine_url = await create_url(user_input)
    try:
        for worker in asyncio.as_completed(corrutine_url):
            resultat = await worker
    except Exception as e:
        print(f"{e}")

async def http_parser(url):
    async with aiohttp.ClientSession() as session:
        print("Establishing a connection")
        async with session.get(url) as response:
            result = await response.json()
            await parser_PB_in_session(result, ["EUR","USD"])


async def parser_PB_in_session(data, currency):
    date_json = data["date"]
    currency_list = []
    for i in data["exchangeRate"]:
        if i["currency"] in currency:
            currency_pb = f"{i["currency"]}"
            purchase_pb = f"{i["purchaseRate"]}"
            sale_pb = f"{i["saleRate"]}"
            currency_list.append({
                f"{date_json}":{
                    f"{currency_pb}": f"sale: {sale_pb}, purchase: {purchase_pb}"
                }
            })
    print(currency_list)

async def create_url(user_input):
    url_list = []
    current_date = datetime.now().date()

    for i in range(user_input):
        parse_date = current_date - timedelta(days=i)
        print(parse_date)
        year, mounth, day = str(parse_date).split("-")
        url_date = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={day}.{mounth}.{year}"
        url_list.append(http_parser(url_date))
    return url_list

def start():
    timer = time()
    if len(sys.argv) != 2:
        print("Not enough parameters")
    else:
        if int(sys.argv[1]) <= 10:
            target_count = sys.argv[1]
            r = asyncio.run(main(int(target_count)))
        else:
            print("Number of days should not exceed 10")
    
    print(f"Execution time: {time()- timer}")


if __name__ == "__main__":
    start()

