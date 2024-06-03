import pymongo
import sys
from os import environ
from dotenv import load_dotenv


load_dotenv()

def connect_NoSQL(collection_name):
    uri = environ.get("uri")
    # Create a new client and connect to the server

    try:
        client = pymongo.MongoClient(uri)

    # return a friendly error if a URI error is thrown
    except pymongo.errors.ConfigurationError:
        print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
        sys.exit(1)
    db = client.Boozevilla
    my_collection = db[collection_name]
    return my_collection


def insert_data(my_collection, data):
    # drop the collection in case it already exists
    try:
        my_collection.drop()

    # return a friendly error if an authentication error is thrown
    except pymongo.errors.OperationFailure:
        print("An authentication error was received. Are your username and password correct in your connection string?")
        sys.exit(1)

    # INSERT DOCUMENTS
    #
    # You can insert individual documents using collection.insert_one().
    # In this example, we're going to create four documents and then
    # insert them all with insert_many().

    try:
        result = my_collection.insert_many(data)

    # return a friendly error if the operation fails
    except pymongo.errors.OperationFailure:
        print("An authentication error was received. Are you sure your database user is authorized to perform write "
              "operations?")
    else:
        inserted_count = len(result.inserted_ids)
        print(f"I inserted {inserted_count} documents.")

        print("\n")
