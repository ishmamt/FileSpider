# ~~ made by sed_cat ~~

# This only encrypts and decrypts the password
# Decryption is to be only used for debugging

def pass_encryption(password):
    key = len(password)
    new_pass = ''
    for char in password:
        shifted_char = ord(char) + key  # shifting each char of the password by the key
        if shifted_char > 126:
            shifted_char = shifted_char - 127 + 32  # for wrapping around
        new_pass += chr(shifted_char)
    return new_pass


def pass_decryption(password):
    # similar to encryption
    key = len(password)
    original = ''
    for char in password:
        shifted_char = ord(char) - key
        if shifted_char < 32:
            shifted_char = 127 - (32 - shifted_char)
        original += chr(shifted_char)
    return original
