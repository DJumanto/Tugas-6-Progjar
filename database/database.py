import json
import os
from pathlib import Path
from operator import itemgetter


class Database:
    def __init__(self, table_name):
        self.table_name = table_name
        base_path = Path(__file__).parent.absolute()
        self.file_name = Path(__file__).joinpath(base_path, self.table_name)
        self.data = self.read_db()

    # read_db reads data from file
    def read_db(self):
        try:
            f = open(self.file_name, "r")
            file_data = json.load(f)
            f.close()
            return file_data["data"]
        except Exception as e:
            print("Tidak dapat membaca file ", e)
            return

    # write_db writes data in the file
    def write_db(self):
        try:
            f = open(self.file_name, "w")
            f.truncate(0)
            f.write(json.dumps({"data": self.data}, indent=4))
            f.close()
        except Exception as e:
            print("Tidak dapat menulis file ", e)
            return

    # get_all returns all the data in the database
    def get_all(self):
        return self.data

    # is_exists checks if a data exists matching by the key and value
    def is_exists(self, key, value):
        return value in [data[key] for data in self.data]

    # get_by_key_value returns a data by the matching key and value
    def get_by_key_value(self, key, value):
        lookup = {d[key]: d for d in self.data}
        return lookup.get(value)
    
    def getall_by_key_value(self, key, value):
        result = []
        for obj in self.data:
            if obj.get(key) == value:
                result.append(obj)
        return result
        # lookup = {d[key]: d for d in self.data}
        # return lookup.get(value)
    


    # insert_data inserts a new data and writes it into the database
    def insert_data(self, new_data):
        self.data.append(new_data)
        self.write_db()

    # get_sorted returns the data of a table in a sorted order by one of its key
    def get_sorted(self, key, asc=False):
        return sorted(self.data, key=itemgetter(key), reverse=(not asc))


if __name__ == "__main__":
    db = Database("user.json")
    print(db.get_all())
    db.insert_data({"username": "aaa", "password": "123"})
    print(db.get_all())
    print(db.get_sorted("username", True)[0])
    print(db.is_exists("username", "aaa"))
    print(db.get_by_key_value("username", "user"))
