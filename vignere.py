NUMERIC = "1234567890"
ALPHANUMERIC = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"


def is_numeric(string):
    try:
        float(string)
        return True
    except:
        return False

# This method encrypts a given plaintext using the Vignere cipher, and the given key.
# It is able to detect if the plaintext is purely numeric (with decimal points), in which case it uses a numeric "alphabet". 
# Otherwise, it uses an alphanumeric "alphabet".
# The encryption ignores foreign characters, simply passing them through to the output.
#   plaintext: the string to encrypt. Can contain any characters found in the alphabet.
#   key: the key for encryption.
def encrypt(plaintext, key):
    alphabet = NUMERIC if is_numeric(plaintext) else ALPHANUMERIC
    return_array = []
    key_i = 0
    for plain_char in plaintext:
        key_char = key[key_i]
        try: 
            plain_index = alphabet.index(plain_char)
        except ValueError:
            return_array.append(plain_char)
            continue
        key_index = alphabet.index(key_char)
        cipher_index = plain_index + key_index
        cipher_char = alphabet[cipher_index % len(alphabet)]
        return_array.append(cipher_char)

        key_i = (key_i + 1) % len(key)
    return ''.join(return_array)


# This method does the exact opposite of the above method. It is used to decrypt Vignere encoded ciphertexts with a given key.
#   ciphertext: the string to decrypt. Can contain any characters found in the alphabet.
#   key: the key for decryption.
def decrypt(ciphertext, key):
    alphabet = NUMERIC if is_numeric(ciphertext) else ALPHANUMERIC
    return_array = []
    key_i = 0
    for cipher_char in ciphertext:
        key_char = key[key_i]
        cipher_index = alphabet.index(cipher_char)
        key_index = alphabet.index(key_char)
        plain_index = cipher_index - key_index
        plain_char = alphabet[plain_index]
        return_array.append(plain_char)

        key_i = (key_i + 1) % len(key)
    return ''.join(return_array)
