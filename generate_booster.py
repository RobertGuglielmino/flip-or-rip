from get_card_info import get_card_info
from get_set_date import get_set_date
from datetime import date
import json
import random
import asyncio

#move to const file eventually
MYTHIC_ODDS = 8
BOOLEAN_OUTCOME = [False, True]
BOOSTER_FUN_ODDS_BY_PACK = 3
RARITY_ODDS = [0.7069, 0.2277, 0.0654]
RARITIES = ["common", "uncommon", "rare"]
FOILS_DATE = date(1999, 2, 6)
MYTHICS_DATE = date(2008, 9, 27)
BOOSTER_FUN_DATE = date(2019, 9, 28)
SET_BOOSTERS_DATE = date(2020, 9, 18)
PLAY_BOOSTERS_DATE = date(2024, 2, 9)

def generate_booster(set_code):
    # Retrieve all cards from the specified set
    print("started pack generation")
    set_date = get_set_date(set_code)

    applyFoiling = set_date > FOILS_DATE
    applyMythics = set_date > MYTHICS_DATE
    applyFun = set_date > BOOSTER_FUN_DATE
    
    if applyFoiling:
        print("applying foiling")
    if applyMythics:
        print("applying mythics")
    if applyFun:
        print("applying fun")

    if set_date < SET_BOOSTERS_DATE:
        booster_format = './booster_formats/basic_booster.json'
    elif set_date < PLAY_BOOSTERS_DATE:
        booster_format = './booster_formats/set_booster.json'
    else:
        booster_format = './booster_formats/play_booster.json'
        
    print(f"pulled format: {booster_format}")

    with open(booster_format) as f:
        setJson = json.load(f)

    params = []
    count = 0

    # TODO: treatments, the list, special guests
    for c in setJson['set_booster']['pack_format']:
        card_set_code = set_code
        count += c["cardCount"]
        newParam = f"game:paper"
        if applyFoiling:
            newParam += hitFoil(c["foil_chance"])

        for event in chooseCardOption(c["options"]):
            rarity = event["rarity"]
            if rarity == "land":
                newParam += " type:land"
            elif rarity == "guest":
                card_set_code = "SPG"
            elif rarity == "any":
                rarity = hitAnyRarity()
            temp = [newParam + f" rarity:{rarity} set:{card_set_code}"] * event["count"]
            params += temp
        # query = f"type:land set:{set_code} game:paper"
    # rarity: set: cn: is:foil frame: game:paper is:borderless

    # Apply Booster Fun
    # need to check date of booster for older packs
    if applyFun:
        params = hitBoosterFun(params)

    # The List cards per set

    # SPG cards per set
    # if has SPG, define cn per set.

    #mythic hits 
    if applyMythics:
        params = [hitMythic(param) for param in params]

    # get cards in parallel
    url = 'https://api.scryfall.com/cards/random'
    responses = asyncio.run(get_card_info(url, params))

    #process information for UI
    formattedResponses = [format_card(card) for card in responses]
    # print(responses)

    #shuffle
    random.shuffle(formattedResponses)
    
    print("done!")
    return formattedResponses

def chooseCardOption(e):
    outcomes = [event["cards"] for event in e]
    probabilities = [event["probability"] for event in e]
    return random.choices(outcomes, weights=probabilities, k=1)[0]

def hitBoosterFun(params):
    if random.randrange(BOOSTER_FUN_ODDS_BY_PACK) == 0:
        for i, p in enumerate(params):
            if "rarity:common" in p:
                params[i] = params[i].replace("rarity:common", "rarity:common (frames:showcase or frames:extendedart)")
                break
    return params

def hitAnyRarity():
    outcomes = [rarities for rarities in RARITIES]
    probabilities = [odds for odds in RARITY_ODDS]
    return random.choices(outcomes, weights=probabilities, k=1)[0]

def hitMythic(str):
    if "rare" in str and random.randrange(MYTHIC_ODDS) == 1:
        print("hit mythic")
        return str.replace("rare", "mythic")
    else:
        return str
    
def hitFoil(foilChance):
    return " is:foil" if random.choices(BOOLEAN_OUTCOME, weights=[1 - foilChance, foilChance], k=1)[0] else " is:nonfoil"

def format_card(card_info):
    priceCents = 0
    
    isFoil = card_info["generated_as_foil"]

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
