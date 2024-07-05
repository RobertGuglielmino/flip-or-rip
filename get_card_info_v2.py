import aiohttp
import asyncio

async def get_card_info(url, query_parameters):
    async with aiohttp.ClientSession() as session:
        tasks = [get_data(session, url, params) for params in query_parameters]
        responses = await asyncio.gather(*tasks)
        return responses

async def get_data(session, url, params):
    try:
        async with session.get(url + params) as response:
            response.raise_for_status()
            card_data = await response.json()
            if 'image_uris' not in card_data:
                print(card_data)
            ans = {}
            ans['name'] = card_data['name']
            ans['generated_as_foil'] = True
            if 'prices' in card_data:
                prices = card_data['prices']
                ans['usd'] = prices.get('usd')
                ans['usd_foil'] = prices.get('usd_foil')
                ans['usd_etched'] = prices.get('usd_etched')
            if 'rarity' in card_data:
                ans['rarity'] = card_data['rarity']
            if 'image_uris' not in card_data:
                print(card_data)
            if 'image_status' != 'missing':
                ans['image'] = card_data['image_uris']['normal']
            return ans
    except aiohttp.ClientError as e:
        print(f'Posting data failed: {e}')
        return None
    