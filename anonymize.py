import json

# classes can be "str", "dict", "list", "float", or probably "number"

# simple function that determines if a given object is a "data" object (a string, int, or float) or if it's a structure like a list or dict.
def is_data(object):
    if type(object) is dict or type(object) is list:
        return False
    return True

# this method recurses down an object in order to try and find the field at the given path.
# This given path is in the form of an array of keys, like ["root", "data", 3, "name"] which points to root.data[3].name within the object.
# Once the function locates the object, it calls the callback function on that field, and replaces the value in the field with the callback's return.

def find(object, path, callback):
    # check for errors
    if not path:
        return "Null path!"
    key = path[0]
    if key != '*':
        if type(key) is int:
            if key >= len(object) or key < 0:
                return "KeyError, index out of bounds"
        elif key not in object:
            return "KeyError, key not in dict"

    # base case--we just popped the last key, so we're at the parent of the target
    if len(path) <=  1:
        object[key] = callback(object[key])
        return None
    # Recursive step--we can go further
    else:
        return find(object[key], path[1:], callback)


def anonymizeHelper(item):
    return "placeholder"

def anonymize(object, fields):
    for field_path in fields:
        path = field_path.split('.')
        result = find(object, path, anonymizeHelper)
        if result:
            print(result, field_path)
    
    return object


json_file = open("test_patient.json", "r")
json_data = json_file.read()
json_file.close()

# read json file to object here
json_object = json.loads(json_data)

out_obj = anonymize(json_object, ["resource.resourceType", "resource.id"])

f = open("out.json", "w")
f.write(json.dumps(json_object))
f.close()

