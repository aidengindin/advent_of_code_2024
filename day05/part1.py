from math import floor


def parse(lines):
    rules = []
    updates = []
    for line in lines:
        if "|" in line:
            pages = tuple([int(page) for page in line.split("|")])
            rules.append(pages)
        elif "," in line:
            pages = [int(page) for page in line.split(",")]
            updates.append(pages)
    return rules, updates

def relevant_rules(rules, update):
    return [rule for rule in rules if rule[0] in update and rule[1] in update]

def is_correctly_ordered(rules, update):
    relevant = relevant_rules(rules, update)
    for rule in relevant:
        if update.index(rule[0]) > update.index(rule[1]):
            return False
    return True

def middle_element(update):
    return update[floor(len(update) / 2)]

def middle_sum(rules, updates):
    return sum([middle_element(update) for update in updates if is_correctly_ordered(rules, update)])

with open("day5/input.txt", "r") as f:
    lines = f.readlines()
    rules, updates = parse(lines)
    num = middle_sum(rules, updates)
    print(num)
