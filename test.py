import vignere
import random

json_file = open("Barry322_Pablo44_Russel238_cfb3d38c-e362-b945-3b9c-d5cfe3cde360.json", "r")
string_data = json_file.read()
json_file.close()


replaced = string_data
key = str(random.randint(1000000000, 9999999999))
alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
toEncrypt = ["Barry322", "Pablo44", "Russel238"]
for element in toEncrypt:
    replaced = replaced.replace(element, vignere.encrypt_vignere(element, alphabet, key))

print("The key was: ", key)


f = open("out.txt", "w")
f.write(replaced)
f.close()