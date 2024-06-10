import requests

def get_card_info(card_name):
    # Encode the card name to be URL-friendly
    card_name_encoded = requests.utils.quote(card_name)
    
    # Query Scryfall API for the card
    response = requests.get(f'https://api.scryfall.com/cards/named?exact={card_name_encoded}')
    
    if response.status_code == 200:
        card_data = response.json()
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
        if 'image_status' != 'missing':
            ans['image'] = card_data['image_uris']['png']
            

        return ans
    else:
        return None