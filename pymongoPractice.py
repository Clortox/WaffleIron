import pymongo
import datetime
import pprint


def main():
    # Client is our connection to MongoDB
    client = pymongo.MongoClient()

    # db is the database we are creating / have created
    db = client['test_database']

    # collect is the collection (table) in db
    collect = db['test_user']

    # db and collect DO NOT actually exist until a document has been saved in the collection

    for p in collect.find():
        collect.delete_one(p)

    # To insert into the database, we write a post, which is a .json style object
    post = {"_id": "BrianId",
            "userName": "Brian",
            "email": "Brian@waffles.org",
            "tags": ["python", "waffles", "Kent State"],
            "date": datetime.datetime.utcnow()}

    # Inserting the post into the Mongo Database
    collect.insert_one(post)

    newPost = {
                "_id": "Kelly123",
                "userName": "Kelly",
                "email": "Kelly@waffles.org",
                "text": "Welcome to Wonder Waffles INC",
                "phone": "4408889843",
                "date": datetime.datetime.utcnow()
                }

    collect.insert_one(newPost)

    """
    post = {"_id": "BrianID",
            "userName": "Brian",
            "email": "Brian@waffles.org",
            "tags": ["python", "waffles", "Kent State"],
            "date": datetime.datetime.utcnow()}

    # Inserting the post into the Mongo Database
    collect.insert_one(post)
    """

    # Print all entries in the collection
    for p in collect.find():
        pprint.pprint(p)

    # Attempt at editing saved document.
    post = collect.find_one({"_id": "BrianId"})
    collect.update_one(post, {'$set': {"userName": "NotBrian"}})


    # Print all entries in the collection
    for p in collect.find():
        pprint.pprint(p)


if __name__ == "__main__":
    main()
