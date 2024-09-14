#!/usr/bin/python3


from json import dump, load
from os.path import exists


class FileStorage:

    # Private class attributes
    # __ means they're private & shouldn't be accessed outside the class
    # __file_path: string is the path to the JSON file
    # __objects: dictionary will store all objects by <class name>.id
    #            example: to store a BaseModel object with id=12121212,
    #                the key will be BaseModel.12121212
    __file_path = "file.json"
    __objects = {}

    # Public instance methods
    def all(self):
        # Returns the dictionary __objects
        return FileStorage.__objects

    # By concatenating the class name with the object id, we can create
    #   a unique key to store the object in the dictionary __objects
    def new(self, obj):
        class_name = type(obj).__name__
        object_id = obj.id
        key = class_name + "." + object_id
        FileStorage.__objects[key] = obj

    # Serializes
    # __objects to the JSON file or __file_path to save all objects to a file

    def save(self):

        # Here we have shortend our file name and object
        # Then we'll be iterating through each object to serialize it
        file_name = FileStorage.__file_path
        objects = FileStorage.__objects

        # We convert the value(not key) of each object to readable string
        # Call the to_dict() method from BaseModel to convert EACH object to
        #    a more understandable dictionary with string values,
        #    and save all in a dictionary, so they can be esaly parsed by
        #    programing languges for extraction. A dict inside a dict.
        # We can also write the below 3 lines of code in 1 line through
        # dictionary comprehension: -
        #   obj_dict = {key: value.to_dict for key, value in objects.items()}

        obj_dict = {}
        for key, value in objects.items():
            obj_dict[key] = value.to_dict()

        # We need to open the file in write mode and encode(utf-8) then
        # convert the dictionary to a JSON string and saves it to the file
        # dump() function takes two arguments: 1. the dictionary to be
        # converted to JSON and 2. the file to save it to
        # file_name is the path to the JSON file
        with open(file_name, mode="w", encoding="utf-8") as f:
            dump(obj_dict, f)

    # Deserializes
    # JSON file to __objects. The reload() method will convert the JSON
    #       string back to the dictionary __objects

    def reload(self):

        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.city import City
        from models.state import State
        from models.amenity import Amenity
        from models.review import Review

        # This is the dictionary we will be loading from the JSON file
        file_name = FileStorage.__file_path
        # We need to check if the file exists before we try to open it but we
        #   don't do anything if it doesn't exist
        if exists(file_name):
            # Here we open the file but since we are only reading from it,
            # We don't need to specify a mode or encode(cuz it's the default)
            with open(file_name) as f:
                obj_dict = load(f)
                # print(obj_dict)
        # At this point, we're able to print the JSON file but are still
        # in a dictionary form and need to be converted to object form

            for value in obj_dict.values():
                # This gets the class name of the object & the eval() function
                # makes sure the class type is "type" and not a string
                class_name = eval(value["__class__"])
                del value["__class__"]
                # Now we want to create a new object from the dictionary values
                # by passing them as keyword arguments to BaseModel, user...etc
                # Cuz both in the classes & here objects are changed to to_dict
                #   so when passed through ** we get new objects
                obj = class_name(**value)
                # Here we call on the new method from above because we want to
                # pass each newly iterated object to __objects
                self.new(obj)
