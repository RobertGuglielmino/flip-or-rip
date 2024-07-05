from get_card_info_v2 import get_card_info
from get_set_date import get_set_date
from datetime import date
import json
import random
import asyncio

def generate_booster(set_code):
    with open(f'./magic_set_jsons/{set_code}.json', encoding="utf8") as f:
        setJson = json.load(f)

    boosterOptions = setJson["data"]["booster"]

    boosterType = boosterOptions["play"]
    boosterSheets = boosterType["sheets"]

    chosenBoosterStructure = chooseWeightedEvent(boosterType["boosters"])

    boosterPackByUUID = []
    boosterPackByFoils = []
    for slot in chosenBoosterStructure.keys():
        numCards = chosenBoosterStructure[slot]
        print(numCards)
        for _ in range(numCards):
            boosterPackByUUID += chooseCardInSheet(boosterSheets[slot]["cards"])
            boosterPackByFoils += [boosterSheets[slot]["foil"]]

    #TODO combine ids with foil statu

    boosterPackByScryfallID = list(map(lambda card: card["identifiers"]["scryfallId"], filter(lambda x: x["uuid"] in boosterPackByUUID, setJson["data"]["cards"])))
    
    # get cards in parallel
    url = 'https://api.scryfall.com/cards/'
    responses = asyncio.run(get_card_info(url, boosterPackByScryfallID))

    #process information for UI
    formattedResponses = [format_card(card) for card in responses]
    # print(responses)

    #shuffle
    random.shuffle(formattedResponses)
    
    print("done!")
    return formattedResponses



def chooseCardInSheet(e):
    outcomes = [event for event in e.keys()]
    probabilities = [event for event in e.values()]
    return random.choices(outcomes, weights=probabilities, k=1)

def chooseWeightedEvent(e):
    outcomes = [event["contents"] for event in e]
    probabilities = [event["weight"] for event in e]
    return random.choices(outcomes, weights=probabilities, k=1)[0]

def format_card(card_info):
    priceCents = 0
    
    isFoil = True

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


# # get cards in parallel
# url = 'https://api.scryfall.com/cards/random'
# responses = asyncio.run(get_card_info(url, params))

# #process information for UI
# formattedResponses = [format_card(card) for card in responses]
# # print(responses)

# #shuffle
# random.shuffle(formattedResponses)

# print("done!")
# return formattedResponses

# def format_card(card_info):
#     priceCents = 0
    
#     isFoil = card_info["generated_as_foil"]

#     if isFoil and card_info['usd_foil']:
#         priceCents = int(card_info['usd_foil'][-2:]) + (int(card_info['usd_foil'][:-3]) * 100)
#     elif card_info['usd']:
#         priceCents = int(card_info['usd'][-2:]) + (int(card_info['usd'][:-3]) * 100)

#     return {
#         'name': card_info['name'],
#         'foil': isFoil,
#         'cents': priceCents,
#         'rarity': card_info['rarity'],
#         'image': card_info['image']
#     }
