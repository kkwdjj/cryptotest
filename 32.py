from sympy import mod_inverse

p = 65537
q = 101
n = p * q
et = (p - 1) * (q - 1)
e = 3
d = mod_inverse(e, et)

print(f"public key: [{e}, {n}]")
print(f"private key: [{d}, {n}]")

x = "hello"
# print("testnum:42")
# c=42**e%n
# m=c**d%n

encrypted_chars = []
for char in x:
    char_int = ord(char)
    
    encrypted_int = pow(char_int, e, n)
    encrypted_chars.append(encrypted_int)

decrypted_chars = []
for encrypted_int in encrypted_chars:
    decrypted_int = pow(encrypted_int, d, n)
    decrypted_char = chr(decrypted_int)
    decrypted_chars.append(decrypted_char)

decrypted_message = "".join(decrypted_chars)
print("Decrypted message:", decrypted_message)
