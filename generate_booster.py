from mtgsdk import Card
from mtgsdk import Set
from get_card_info import get_card_info
import random

def generate_booster(set_code):
    # Retrieve all cards from the specified set
    cards = Card.where(set=set_code).all()

    pack = []
    FOIL_ODDS = 67

    # newCommons = Card.where(set=set_code).where(rarity='Common').where(pageSize=10).where(random=10).all()

    # print(Set.find('ktk'))

    # Separate cards by rarity
    commons = [card for card in cards if card.rarity == 'Common' and card.rarity != 'Basic Land']
    uncommons = [card for card in cards if card.rarity == 'Uncommon']
    rares = [card for card in cards if card.rarity == 'Rare']
    mythics = [card for card in cards if card.rarity == 'Mythic']
    lands = [card for card in cards if card.type == 'Land']

    booster_pack = [random.choice(lands)] + random.sample(commons, 10) + random.sample(uncommons, 3) + [random.choice(rares + mythics)]

    for card in booster_pack:
        isFoil = random.randrange(FOIL_ODDS) == 1

        priceDollars = 0
        priceCents = 0

        # make async
        card_info = get_card_info(card.name)

        if isFoil and card_info['usd_foil']:
            priceDollars = int(card_info['usd_foil'][:-3])
            priceCents = int(card_info['usd_foil'][-2:])
        elif card_info['usd']:
            priceDollars = int(card_info['usd'][:-3])
            priceCents = int(card_info['usd'][-2:])


        # print(card_info)

        pack.append({
            'name': card.name,
            'foil': isFoil,
            'dollars': priceDollars,
            'cents': priceCents,
            'image': card_info['image']
        })

    return pack