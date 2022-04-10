from pymongo import MongoClient


def setPath(cID):
    return MongoClient()['WaffleIron_DB'][cID]


# This will be called when a new file has been created
def createFile(cID, CRN, cYear, cSem, data={}):
    cTable = setPath(cID)
    file = {
        "_id": CRN,
        "cFields": data,
        "cYear": cYear,
        "cSem": cSem
    }
    cTable.insert_one(file)


# These next functions will be called to update a particular field on a file
def update_cyear(course_ID, CRN, yr):
    cTable = setPath(course_ID)
    file = cTable.find_one({"_id": CRN})
    cTable.update_one(file, {"$set": {"cYear":yr}})


def update_csem(course_ID, CRN, sem):
    cTable = setPath(course_ID)
    file = cTable.find_one({"_id": CRN})
    cTable.update_one(file, {"$set": {"cSem": sem}})


# This function takes a dictionary and edits the stored class fields
# Useful to make one function call to change multiple fields!
def update_cFields(course_ID, CRN, fields):
    data = get_data(course_ID, CRN)

    # First, checks to see which fields must be removed.
    # This is done by seeing which of the stored keys is
    # not present in the dataset being saved / overwritten.
    for key in data.keys():
        if fields.get(key) is None:
            remove_cFields(course_ID, CRN, key)

    # Any other data is set in the cFields. The "$set" command works
    # properly when you take into account Nested Documents.
    # This means that adding new fields and updating new fields will work
    # exactly the same!
    for key in fields.keys():
        add_cFields(course_ID, CRN, key, fields.get(key))


# When arbitrarily updating the data fields, we will need to actively call these functions in order to
# ensure the fields we want added are added, those we want deleted are deleted, and those we want updated
# are updated. NOTE: Adding and Updating will produce the same results!

# Please note, pymongo is treating the stored class fields as a nested document. In order to interact with
# it using pymongo, you need to reference the outer data set name, in this case 'cFields', followed by a
# period, followed by the name of the field you wish to perform queries on, then you provide data if necessary.
# I recommend checking out Nested Documents documentation from MongoDB. I will find a good link for the chat!
def add_cFields(course_ID, CRN, field_key, field_data):
    cTable = setPath(course_ID)
    file = cTable.find_one({"_id": CRN})
    cTable.update_one(file, {"$set": {'cFields.' + field_key: field_data}})


def remove_cFields(course_ID, CRN, field_name):
    cTable = setPath(course_ID)
    file = cTable.find_one({"_id": CRN})
    cTable.update_one(file, {"$unset": {"cFields." + field_name: ""}})


# This next function finds and returns and entire data file from the course
def get_file(course_ID, CRN):
    cTable = setPath(course_ID)
    file = cTable.find_one({"_id": CRN})
    return file


# This next function will only get the class fields from a particular file.
# Particularly useful for updating the class fields...
def get_data(course_ID, CRN):
    cTable = setPath(course_ID)
    file = cTable.find_one({"_id": CRN})
    return file


def main():
    # Uncomment these lines if you need to purge the table
    # you are testing with after an accident!
    # WaffleCourse = setPath('56543')
    # file = WaffleCourse.find_one({'_id': 50000})
    # WaffleCourse.delete_one(file)

    # Course ID will be 56543
    # There will be a series of CRN values passed.
    # A bit of data will be randomly chosen with each test.
    createFile('56543', 50000, 2022, 'SUMMER')
    print(get_file('56543', 50000))
    add_cFields('56543', 50000, "Data", "This is the first field in the file.")
    add_cFields('56543', 50000, "New Data", "A new data point")
    print(get_file('56543', 50000))

    remove_cFields('56543', 50000, "Data")
    print(get_file('56543', 50000))

    add_cFields('56543', 50000, "New Data", 'This is what I meant!')
    print(get_file('56543', 50000))

    add_cFields('56543', 50000, "Data", "The data field has returned! But I will be gone soon...")
    add_cFields('56543', 50000, "Existing Data", "Data with an existential crisis. Do not disturb.")
    update_cFields('56543', 50000, {
                                    "Grades": "This is the grades field, newly added.",
                                    "New Data": 'This is the final new data',
                                    "Waffle Quality Report": "Waffles are wonderful! #WonderWaffles"})
    print(get_file('56543', 50000))

    WaffleCourse = setPath('56543')
    file = WaffleCourse.find_one({'_id': 50000})
    WaffleCourse.delete_one(file)


if __name__ == "__main__":
    main()
