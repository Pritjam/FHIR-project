
# alphabet: the "alphabet" to use for this encryption. In other words, the 
#     set of characters that can be encoded/can be present in the encoded string.
# plaintext: the string to encrypt. Can contain any characters found in the alphabet.
# key: the key for encryption.
def encrypt_vignere(plaintext, alphabet, key):
    return_array = []
    key_i = 0
    for plain_char in plaintext:
        key_char = key[key_i]
        plain_index = alphabet.index(plain_char)
        key_index = alphabet.index(key_char)
        cipher_index = plain_index + key_index
        cipher_char = alphabet[cipher_index % len(alphabet)]
        return_array.append(cipher_char)

        key_i = (key_i + 1) % len(key)
    return ''.join(return_array)

plaintext = "supersecretmessage"
print("Plaintext:", plaintext, "  Encrypts to:", encrypt_vignere(plaintext, "abcdefghijklmnopqrstuvwxyz", "thekey"))

plaintext = "SUPERsecretMESSAGE"
print("Plaintext:", plaintext, "  Encrypts to:", encrypt_vignere(plaintext, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", "thekey"))

plaintext = "5UP3R53cr3tme554g3"
print("Plaintext:", plaintext, "  Encrypts to:", encrypt_vignere(plaintext, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890", "thekey"))


# alphabet: the "alphabet" to use for this decryption. In other words, the 
#     set of characters that can be encoded/can be present in the encoded string.
# ciphertext: the string to decrypt. Can contain any characters found in the alphabet.
# key: the key for decryption.
def decrypt_vignere(ciphertext, alphabet, key):
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

ciphertext = "lbtovqxjvoxkxzwkkc"
print("Ciphertext:", ciphertext, "  Decrypts to:", decrypt_vignere(ciphertext, "abcdefghijklmnopqrstuvwxyz", "thekey"))

ciphertext = "lbTOVQxjvoxkXZWKKc"
print("Ciphertext:", ciphertext, "  Decrypts to:", decrypt_vignere(ciphertext, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", "thekey"))

ciphertext = "n2TcVsljvcxKxb9dkq"
print("Ciphertext:", ciphertext, "  Decrypts to:", decrypt_vignere(ciphertext, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890", "thekey"))