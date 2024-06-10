from mtgsdk import Set

card = Set.find('rna')

print(dir(card))
print(vars(card))