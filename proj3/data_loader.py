import pymongo
from datetime import datetime

def parse_line(line):
    key, value = line.split(': ', 1)
    return key.strip(), value.strip()

def convert_price(value):
    try:
        return float(value)
    except ValueError:
        return value  # Return the original value if it's not a float

def parse_file(file_path):
    with open(file_path, 'r') as file:
        doc = {"product": {}, "review": {}}
        for line in file:
            if line.strip() == "":
                yield doc
                doc = {"product": {}, "review": {}}
            else:
                key, value = parse_line(line)
                if key.startswith('product'):
                    key = key.split('/', 1)[1] 
                    if key == 'price':
                        value = convert_price(value)
                    doc["product"][key] = value
                elif key.startswith('review'):
                    if key == 'review/time':
                        value = datetime.utcfromtimestamp(int(value))
                    if key == 'review/score':
                        value = float(value)

                    key = key.split('/', 1)[1]
                    doc["review"][key] = value
        if doc['product'] or doc['review']:
            yield doc

def insert_into_mongodb(data):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["ArtReviews"]
    collection = db["Reviews"]

    # Drop the existing collection
    collection.drop()

    collection.insert_many(data)

def main():
    file_path = 'Arts.txt'
    data = list(parse_file(file_path))
    insert_into_mongodb(data)

if __name__ == "__main__":
    main()