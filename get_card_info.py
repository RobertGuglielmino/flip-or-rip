import aiohttp
import asyncio

async def get_card_info(url, query_parameters):
    async with aiohttp.ClientSession() as session:
        tasks = [get_data(session, url, params) for params in query_parameters]
        responses = await asyncio.gather(*tasks)
        return responses

async def get_data(session, url, params):
    try:
        async with session.get(url, params="q="+params) as response:
            response.raise_for_status()
            card_data = await response.json()
            if 'image_uris' not in card_data:
                print(card_data)
            ans = {}
            ans['name'] = card_data['name']
            if 'collector_number' in card_data:
                ans['collector_number'] = card_data['collector_number']
            if 'prices' in card_data:
                prices = card_data['prices']
                ans['usd'] = prices.get('usd')
                ans['usd_foil'] = prices.get('usd_foil')
                ans['usd_etched'] = prices.get('usd_etched')
            if 'finishes' in card_data:
                ans['finishes'] = card_data['finishes']
            if 'rarity' in card_data:
                ans['rarity'] = card_data['rarity']

            if 'image_uris' not in card_data:
                print(card_data)
            if 'image_status' != 'missing':
                ans['image'] = card_data['image_uris']['normal']
            ans['generated_as_foil'] = 'is:foil' in params
            return ans
    except aiohttp.ClientError as e:
        print(f'Posting data failed: {e}')
        return None