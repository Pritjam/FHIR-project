import vignere
import random
import json


def expand(object, new_list):
    if type(object) is not list and type(object) is not dict:
        new_list.append(str(object))
    elif type(object) is list:
        for element in object:
            expand(element, new_list)

# this method recurses down an object in order to try and find the field at the given path.
# This given path is in the form of an array of keys, like ["root", "data", 3, "name"] which points to root.data[3].name within the object.
# Once the function locates the object, it calls the callback function on that field, and replaces the value in the field with the callback's return.

def find(object, path, err):
    # check for errors
    if not path:
        return err.append("Error! Null path")
    key = path[0]
    if key != '*':
        if type(key) is int:
            if key >= len(object) or key < 0:
                return err.append("KeyError, index out of bounds")
        elif key not in object:
            return err.append("KeyError, key not in dict")


    if key == '*':
        # wildcard operator
        if len(path) <= 1:
            # need to iteratively return
            if type(object) is list:
                return [element for element in object]
            elif type(object) is dict:
                return [object[key] for key in object]
            else:
                return err.append("Error--wildcard on leaf node!")
        else:
            # need to iteratively recurse
            if type(object) is list:
                return [find(element, path[1:], err) for element in object]
            elif type(object) is dict:
                return [find(object[key], path[1:], err) for key in object]
            else:
                return err.append("Error--could not branch on wildcard! object type is: " + str(type(object)))
    else:
        # regular operation
        if len(path) <= 1:
            return object[key]
        else:
            return find(object[key], path[1:], err)

def find_where(object, field_name, field_value):
    if type(object) is dict:
        if field_name in object:
            if object[field_name] == field_value:
                return object
        for field in object:
            ret = find_where(object[field], field_name, field_value)
            if ret:
                return ret
        print("b")
        return None
    elif type(object) is list:
        for element in object:
            ret = find_where(element, field_name, field_value)
            if ret:
                return ret
        print("c")
        return None
        


def find_strings(object, fields):
    strings = []
    for field_path in fields:
        path = field_path.split('.')
        err = []
        out = find(object, path, err)
        result = []
        expand(out, result)
        if len(err):
            print(err, field_path)
        elif type(result) is list:
            strings.extend(result)
        else:
            strings.append(str(result))
    
    return strings

def anonymize_file(string_data):
    json_object = json.loads(string_data)
    found = find_where(json_object, "resourceType", "Patient")
    strings = find_strings(found, ["name.*.*", "telecom.*.value", "gender", "birthDate", "address.*.extension.*.extension.*.valueDecimal", "address.*.*", "identifier.*.value"])

    replaced = string_data
    key = str(random.randint(1000000000, 9999999999))
    for element in strings:
        replaced = replaced.replace(element, vignere.encrypt(element, key))

    f = open("output/" + str(key) + "_out.json", "w")
    f.write(replaced)
    f.close()

