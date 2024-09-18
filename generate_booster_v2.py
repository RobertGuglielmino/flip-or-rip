import uuid
from get_card_info_v2 import get_card_info
from get_set_date import get_set_date
from datetime import date
from addToCacheTable  import addToCacheTable
import boto3
import json
import random
import asyncio

def generate_booster(set_code, pack_type):
    with open(f'./magic_set_jsons/{set_code}.json', encoding="utf8") as f:
        setJson = json.load(f)

    
    # s3 = boto3.client('s3')
    # setJson = s3.get_object(Bucket='mtg-set-jsons', Key=f'{set_code}.json')
    
    boosterOptions = setJson['Body'].read().decode('utf-8')
    
    json_data = json.loads(boosterOptions)

    boosterType = json_data['data']['booster'][pack_type]
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

    boosterPackByScryfallID = list(map(lambda card: card["identifiers"]["scryfallId"], filter(lambda x: x["uuid"] in boosterPackByUUID, json_data["data"]["cards"])))
    
    boosterPackIdFoil = [{"scryId": boosterPackByScryfallID[i], "foil": boosterPackByFoils[i]} for i in range(len(boosterPackByScryfallID))]
    
    # get cards in parallel
    url = 'https://api.scryfall.com/cards/'
    responses = asyncio.run(get_card_info(url, boosterPackIdFoil))

    #process information for UI
    formattedResponses = [format_card(card) for card in responses]
    random.shuffle(formattedResponses)
    # print(responses)

    #process information for temp stats db
    formatCachePackData = [format_temp_cache_card(card) for card in formattedResponses]
    packId = str(uuid.uuid4())
    print(addToCacheTable(packId, formatCachePackData))
    
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

    return {
        'name': card_info['name'],
        'foil': card_info['isFoil'],
        'cents': card_info['cents'],
        'rarity': card_info['rarity'],
        'image': card_info['image'],
        'cf_image': card_info['cf_image'],
        'scryfallId': card_info['scryfallId']
    }

def format_temp_cache_card(card):
    return {
        'name': card['name'],
        'price': int(card['cents']),
        'scryfallId': card['scryfallId']
    }