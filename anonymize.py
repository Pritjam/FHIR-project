import vignere
import random
import json
import os.path as path

# This method turns a nested list structure into a plain list. 
# For example, if there is a list within a list, this method "unrolls" that list to a single-layer list with all elements of the outer and inner lists in it. 
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


# this method allows a query into an object, to find a sub-object within it where a certain field has a certain value.
# It can be though of as an SQL query like SELECT * FROM object WHERE object[field_name] == field_value

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
        

# This method returns the values of certain specified fields in an object.
# Fields are specified using the "." operator, such as "parent.child.property". 
# The wildcard operator, the asterisk "*" can be used to operate on multiple parts of an object at the same time.
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


# This method anonymizes a given JSON string and writes the output JSON string to a file.
# The file name is determined by the randomly generated Vignere key.
# The output directory to put the anonymized file is specified by the parameter "output_dir".
def anonymize_file(string_data, output_dir, paths):
    json_object = json.loads(string_data)
    found = find_where(json_object, "resourceType", "Patient")
    strings = find_strings(found, paths)

    replaced = string_data
    key = str(random.randint(1000000000, 9999999999))
    for element in strings:
        replaced = replaced.replace(element, vignere.encrypt(element, key))

    f = open(path.join(output_dir, str(key) + "_out.json"), "w")
    f.write(replaced)
    f.close()

