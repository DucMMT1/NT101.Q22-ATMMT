from Crypto.Cipher import DES
import binascii

def to_binary(data):
    """Chuyển đổi bytes sang chuỗi nhị phân 64-bit"""
    return ''.join(format(b, '08b') for b in data)

def calculate_hamming_distance(bin1, bin2):
    """Đếm số bit khác nhau (Hamming Distance)"""
    return sum(c1 != c2 for c1, c2 in zip(bin1, bin2))

def run_des_avalanche(plain1, plain2, key_str):
    key = key_str.encode('ascii')
    cipher = DES.new(key, DES.MODE_ECB)
    
    ct1 = cipher.encrypt(plain1.encode('ascii'))
    ct2 = cipher.encrypt(plain2.encode('ascii'))
    bin1 = to_binary(ct1)
    bin2 = to_binary(ct2)
    
    distance = calculate_hamming_distance(bin1, bin2)
    percentage = (distance / 64) * 100
    
    print(f"--- Ket qua voi Key (MSSV): {key_str} ---")
    print(f"Plaintext 1: {plain1} -> Ciphertext (Hex): {ct1.hex()}")
    print(f"Plaintext 2: {plain2} -> Ciphertext (Hex): {ct2.hex()}")
    print(f"Hamming Distance: {distance} bits")
    print(f"Avalanche Ratio: {percentage:.2f}%\n")
    return percentage

p1 = "STAYHOME"
p2 = "STAYHOMA" 
mssvs = ["24520330", "24520313"]

for mssv in mssvs:
    run_des_avalanche(p1, p2, mssv)