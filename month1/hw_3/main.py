import csv
import json
from csv import DictReader

from files import JSON_FILE_PATH
from files import JSON_FILE_RESULT
from files import CSV_FILE_PATH

with open(JSON_FILE_PATH, "r") as f:
    users = json.load(f)

with open(CSV_FILE_PATH, "r") as file:
    books = list(csv.DictReader(file))

books_per_users = len(books) // len(users)

books_remain = len(books) % len(users)

out_users_data = []

for user in users:
    user_books = []
    for i in range(books_per_users):
        user_books.append(books.pop(0))

    if books_remain > 0:
        user_books.append(books.pop(0))
        books_remain -= 1

    out_users_data.append({"name": user["name"],
                           "gender": user["gender"],
                           "address": user["address"],
                           "age": user["age"],
                           "books": user_books})

with open(JSON_FILE_RESULT, "w") as outfile:
    json.dump(out_users_data, outfile, indent=4)
