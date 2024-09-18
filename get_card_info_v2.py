import aiohttp
import asyncio

async def get_card_info(url, query_parameters):
    async with aiohttp.ClientSession() as session:
        tasks = [get_data(session, url, params) for params in query_parameters]
        responses = await asyncio.gather(*tasks)
        return responses

async def get_data(session, url, params):
    try:
        async with session.get(url + params["scryId"]) as response:
            response.raise_for_status()
            isFoil = params["foil"]
            card_data = await response.json()
            
            ans = {}
            ans['name'] = card_data['name']
            ans['isFoil'] = isFoil
            ans['scryfallId'] = card_data['id']
            ans['scryId'] = card_data['id']
            if 'prices' in card_data:
                usdPrice = card_data['prices'].get('usd_foil') if isFoil else card_data['prices'].get('usd')
                ans['cents'] = 0 if not usdPrice else int(usdPrice[-2:]) + (int(usdPrice[:-3]) * 100)
            if 'rarity' in card_data:
                ans['rarity'] = card_data['rarity']
            if 'card_faces' in card_data:
                print("hit a double faced card, replacing with Phantom Nishoba")
                ans['image'] = "https://cards.scryfall.io/normal/front/5/6/56ebc372-aabd-4174-a943-c7bf59e5028d.jpg?1562629953"
                ans['cf_image'] = "https://d3vjinhen5j20w.cloudfront.net/56ebc372-aabd-4174-a943-c7bf59e5028d.jpg"
            else:
                ans['image'] = card_data['image_uris']['normal']
                ans['cf_image'] = f"https://d3vjinhen5j20w.cloudfront.net/{card_data['id']}.jpg"
            return ans
    except aiohttp.ClientError as e:
        print(f'Posting data failed: {e}')
        return None
    