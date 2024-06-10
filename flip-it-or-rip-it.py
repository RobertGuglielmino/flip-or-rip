from mtgsdk import Card
from mtgsdk import Set
from generate_booster import generate_booster


flipped_cards = []
ripped_cards = []
lost_dollars = 0
lost_cents = 0


def flip_it(list, card):
    flipped_cards.append(list.pop(card))

def rip_it(list, card, dollars, cents):
    ripped_card = list.pop(card)
    dollars += int(ripped_card['price'][:-3])
    cents += int(ripped_card['price'][-2:])
    print(cents)
    ripped_cards.append(ripped_card)

booster = generate_booster('AFR')

dollars = 0
cents = 0
for card in booster:
    dollars += int(card['dollars'])
    cents += int(card['cents'])
dollars += (cents - (cents % 60)) / 60
cents = cents % 60 
print(int(dollars))
print(cents)
print([c for c in booster if c['foil']])
print("SORTED")
# print(sorted(booster, key = lambda b: (b['dollars'], b['cents'])))

