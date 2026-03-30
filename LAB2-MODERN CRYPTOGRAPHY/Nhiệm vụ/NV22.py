from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii

key = b'1234567890123456' # [cite: 325, 326]
plaintext = b"UIT_LAB_UIT_LAB_UIT_LAB_UIT_LAB_" # [cite: 317, 327]

# --- CHẾ ĐỘ AES-ECB ---
cipher_ecb = AES.new(key, AES.MODE_ECB) # [cite: 330]
ct_ecb = cipher_ecb.encrypt(plaintext) # [cite: 330]

# --- CHẾ ĐỘ AES-CBC ---
iv = b'0000000000000000' 
cipher_cbc = AES.new(key, AES.MODE_CBC, iv)
ct_cbc = cipher_cbc.encrypt(plaintext)
print(f"Plaintext: {plaintext.decode()}")
print("-" * 50)

print(f"ECB Ciphertext (Hex): {ct_ecb.hex()}")
print(f"Block 1 (ECB): {ct_ecb[:16].hex()}")
print(f"Block 2 (ECB): {ct_ecb[16:].hex()}")
if ct_ecb[:16] == ct_ecb[16:]:
    print("=> Nhận xét: Hai khối bản mã GIỐNG HỆT NHAU")

print("-" * 50)

print(f"CBC Ciphertext (Hex): {ct_cbc.hex()}")
print(f"Block 1 (CBC): {ct_cbc[:16].hex()}")
print(f"Block 2 (CBC): {ct_cbc[16:].hex()}")
if ct_cbc[:16] != ct_cbc[16:]:
    print("=> Nhận xét: Hai khối bản mã KHÁC NHAU")