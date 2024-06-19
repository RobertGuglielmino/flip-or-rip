from get_card_info import get_card_info
import json
import random
import time
import asyncio
import urllib

MYTHIC_ODDS = 8

def generate_booster(set_code):
    # Retrieve all cards from the specified set
    print("started pack generation")

    with open('./booster_formats/set_booster.json') as f:
        setJson = json.load(f)

    params = []
    count = 0
    t0 = time.time()

    # does booster generate based off of a reference json 
    # TODO: treatments, foil chances
    for c in setJson['set_booster']['pack_format']:
        count += c["cardCount"]
        newParam = f"set:{set_code} game:paper"
        if c["type"] == "static":
            if c["rarity"] == "land":
                newParam += " type:land"
            elif c["rarity"] == "rare":
                newParam += f" rarity:rare"
            params.append(newParam)
        elif c["type"] == "spread":
            outcomes = [event["cards"] for event in c["options"]]
            probabilities = [event["probability"] for event in c["options"]]
            selected_event = random.choices(outcomes, weights=probabilities, k=1)[0]
            for event in selected_event:
                respRarity = event["rarity"]
                temp = [newParam + f" rarity:{respRarity}"] * event["count"]
                params += temp
        # query = f"type:land set:{set_code} game:paper"
    # rarity: set: cn: is:foil frame: game:paper

    #mythic hits 
    upgradedParams = [chanceMythic(param) for param in params]

    # get cards in parallel
    url = 'https://api.scryfall.com/cards/random'
    responses = asyncio.run(get_card_info(url, upgradedParams))

    #process information for UI
    formattedResponses = [format_card(card) for card in responses]

    #shuffle
    random.shuffle(formattedResponses)
    
    print("done!")
    return formattedResponses




def chanceMythic(str):
    if "rare" in str and random.randrange(MYTHIC_ODDS) == 1:
        print("hit mythic")
        return str.replace("rare", "mythic")
    else:
        return str


def format_card(card_info):
    priceCents = 0
    
    if "foil" in card_info["finishes"]:
        isFoil = True
    else:
        isFoil = False

    if isFoil and card_info['usd_foil']:
        priceCents = int(card_info['usd_foil'][-2:]) + (int(card_info['usd_foil'][:-3]) * 100)
    elif card_info['usd']:
        priceCents = int(card_info['usd'][-2:]) + (int(card_info['usd'][:-3]) * 100)

    return {
        'name': card_info['name'],
        'foil': isFoil,
        'cents': priceCents,
        'rarity': card_info['rarity'],
        'image': card_info['image']
    }
