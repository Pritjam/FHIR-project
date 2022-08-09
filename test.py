import anonymize
import sys

if len(sys.argv) < 3:
    print("Please provide a filename or directory to anonymize. Example: \'" + sys.argv[0] + " -f test_file.json\'")
    quit()

if sys.argv[1] == "-f":
    try:
        json_file = open(sys.argv[2], "r")
    except:
        print("Error, file \'" + str(sys.argv[2]) + "\' not found!")
        quit()

    string_data = json_file.read()
    json_file.close()
    
    anonymize.anonymize_file(string_data)

elif sys.argv[1] == "-d":
    print("-d functionality not yet implemented")
    quit()

else:
    print("Argument \'" + sys.argv[1] + "\' isn't defined. Please use -f for a file or -d for a directory.")
    quit()

