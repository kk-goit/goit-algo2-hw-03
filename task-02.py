import csv
import timeit
from BTrees.OOBTree import OOBTree


def add_item_to_tree(tree: OOBTree, item: dict):
    tree[item["ID"]] = item


def add_item_to_price_tree(tree: OOBTree, item: dict):
    if item["Price"] not in tree:
        tree[item["Price"]] = [item]
    else:
        tree[item["Price"]].append(item)


def add_item_to_dict(the_dict: dict, item: dict):
    the_dict[item["ID"]] = item


def range_query_tree(atree: OOBTree, min_price: float, max_price: float) -> list:
    rezult = []
    for key in atree.keys():
        if atree[key]["Price"] >= min_price and atree[key]["Price"] <= max_price:
            rezult.append(atree[key])
    return rezult


def range_query_price_tree(atree: OOBTree, min_price: float, max_price: float) -> list:
    rezult = []
    for price, items in atree.iteritems(min_price, max_price):
        rezult.extend(items)
    return rezult


def range_query_dict(adict: dict, min_price: float, max_price: float) -> list:
    rezult = []
    for key in adict.keys():
        if adict[key]["Price"] >= min_price and adict[key]["Price"] <= max_price:
            rezult.append(adict[key])
    return rezult


the_tree = OOBTree()
price_tree = OOBTree()
the_dict = {}

headers = []
min_price = float("inf")
max_price = 0
with open("generated_items_data.csv", "r") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")
    for row in csvreader:
        if not headers:
            headers = row
            continue

        obj = {}
        for key in headers:
            obj[key] = row[headers.index(key)]
            if key == "ID":
                obj[key] = int(obj[key])
            elif key == "Price":
                obj[key] = float(obj[key])
                min_price = min(min_price, obj[key])
                max_price = max(max_price, obj[key])

        add_item_to_tree(the_tree, obj)
        add_item_to_price_tree(price_tree, obj)
        add_item_to_dict(the_dict, obj)

print(f"Загальний ціновий діапозон: {min_price} - {max_price}")

min_price = 20
max_price = 120
number_of_runs = 100
repeat_times = 1


def setup_tree():
    global the_tree, min_price, max_price
    return the_tree, min_price, max_price


timer = timeit.Timer(
    lambda: range_query_tree(*setup_tree()),
)

results = timer.repeat(repeat=repeat_times, number=number_of_runs)

average_times = [result / number_of_runs for result in results]

print(f"Разрахунок для OOBTree(idexed by ID) {number_of_runs*repeat_times} запусків")
print(f"Середный час виконання: {min(average_times):.6f} секунд")


def setup_dict():
    global the_dict, min_price, max_price
    return the_dict, min_price, max_price


timer = timeit.Timer(
    lambda: range_query_dict(*setup_dict()),
)

results = timer.repeat(repeat=repeat_times, number=number_of_runs)

average_times = [result / number_of_runs for result in results]

print(f"Разрахунок для dict {number_of_runs*repeat_times} запусків")
print(f"Середный час виконання: {min(average_times):.6f} секунд")


def setup_price_tree():
    global price_tree, min_price, max_price
    return price_tree, min_price, max_price


timer = timeit.Timer(
    lambda: range_query_price_tree(*setup_price_tree()),
)

results = timer.repeat(repeat=repeat_times, number=number_of_runs)

average_times = [result / number_of_runs for result in results]

print(
    f"Разрахунок для OOBTree(indexed by price) {number_of_runs*repeat_times} запусків"
)
print(f"Середный час виконання: {min(average_times):.6f} секунд")
