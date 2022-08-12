import os
import os.path as path
import sys
import anonymize
import time

if "--help" in sys.argv:
    print("\nThis tool monitors a folder for new .json files of HL7 FHIR standard. It then anonymizes these files using a randomly generated key, to remove all idenitifying data.")
    print("\nUsage: 'py monitor_encrypt.py <config file> <Input directory> <Archive directory> <Output directory> [Error directory]'")
    print("\nThe tool continuously monitors the input directory for new files. It then anonymizes any files found, and puts the anonymized forms into the output directory.\nIt also archives the unanonymized files to the archive directory.")
    print("The anonymization is handled via a Vignere cipher, using a randomly generated key. This allows for de-anonymization if needed, via the key which is in the output filename.")
    quit()

if len(sys.argv) < 5:
    print("Please provide an input directory to monitor, an archive directory to move unanonymized files to, and an output directory to move anonymized files to.")
    print("use --help to see the usage message.")
    quit()


# actually ecrypting files
if len(sys.argv) >= 5:
    # check config file
    if not path.isfile(sys.argv[1]):
        print("Invalid config file!")
        quit()
    # check input dir
    if not path.isdir(sys.argv[2]):
        print("Invalid input directory")
        quit()
    # check archive dir
    if not path.isdir(sys.argv[3]):
        print("Invalid archive directory")
        quit()
    # check output dir
    if not path.isdir(sys.argv[4]):
        print("Invalid output directory")
        quit()

do_errors = False
# check if we also have an error directory specified
if len(sys.argv) > 5:
    # check error dir
    if not path.isdir(sys.argv[5]):
        print("Invalid error directory")
        quit()
    do_errors = True

input_dir = sys.argv[2]
output_dir = sys.argv[4]
archive_dir = sys.argv[3]

paths_file = open(sys.argv[1])
fields_to_anonymize = [line.strip() for line in paths_file]
paths_file.close()
    
    
print("Monitoring the input now")
while True:
    time.sleep(3)
    # iterate over all json files in input dir, anonymize them, and archive them
    for file in os.listdir(sys.argv[2]):
        if file.endswith(".json"):
            json_file = open(path.join(input_dir, file), "r")
            string_data = json_file.read()
            json_file.close()
            try:
                anonymize.anonymize_file(string_data, output_dir, fields_to_anonymize)
            except:
                if do_errors:
                    os.rename(path.join(input_dir, file), path.join(sys.argv[5], file))
                continue
            os.rename(path.join(input_dir, file), path.join(archive_dir, file))