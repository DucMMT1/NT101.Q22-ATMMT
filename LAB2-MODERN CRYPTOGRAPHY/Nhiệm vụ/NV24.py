from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

BLOCK_SIZE = 16  # 16 bytes (128-bit)
SECRET_KEY = b'1234567890123456'   # Khóa 128-bit
INIT_VECTOR = b'abcdefghijklmnop'  # IV 128-bit

# Sinh dữ liệu ngẫu nhiên (plaintext)
def generate_random_data(size=1000): # 
    return os.urandom(size)

# KHỞI TẠO CIPHER
def create_cipher(mode: str):
    if mode == 'ECB':
        return AES.new(SECRET_KEY, AES.MODE_ECB)

    elif mode == 'CBC':
        return AES.new(SECRET_KEY, AES.MODE_CBC, INIT_VECTOR)

    elif mode == 'CFB':
        return AES.new(SECRET_KEY, AES.MODE_CFB, INIT_VECTOR, segment_size=128)

    elif mode == 'OFB':
        return AES.new(SECRET_KEY, AES.MODE_OFB, INIT_VECTOR)

    else:
        raise ValueError(f"Mode không hợp lệ: {mode}")

# LỖI TRÊN CIPHERTEXT
# Đảo 1 bit tại vị trí byte_index (Mặc định byte 26 - index 25)
def flip_bit(cipher_bytes: bytearray, byte_index=25): # [cite: 371]
    cipher_bytes[byte_index] ^= 1
    return cipher_bytes

# ĐẾM BLOCK BỊ LỖI
# So sánh từng block 16 byte để đếm block bị sai
def count_corrupted_blocks(original: bytes, decrypted: bytes):
    corrupted = 0
    for i in range(0, len(original), BLOCK_SIZE):
        original_block = original[i:i + BLOCK_SIZE]
        decrypted_block = decrypted[i:i + BLOCK_SIZE]

        if original_block != decrypted_block:
            corrupted += 1
    return corrupted

# MÔ PHỎNG LAN TRUYỀN LỖI
def simulate_error(mode: str):
    """
    Mô phỏng:
    1. Sinh dữ liệu & Padding
    2. Mã hóa
    3. Gây lỗi 1 bit
    4. Giải mã
    5. Đếm block lỗi
    """

    # 1. Sinh dữ liệu 1000 byte 
    raw_plaintext = generate_random_data()
    plaintext = pad(raw_plaintext, BLOCK_SIZE) 

    # 2.Mã hóa bằng AES-128
    encrypt_cipher = create_cipher(mode)
    ciphertext = bytearray(encrypt_cipher.encrypt(plaintext))

    # 3.Làm hỏng bản mã bằng cách đảo 1 bit tại byte thứ 26 
    corrupted_cipher = flip_bit(ciphertext)

    # 4.Giải mã bản mã đã bị lỗi 
    decrypt_cipher = create_cipher(mode)
    decrypted_text = decrypt_cipher.decrypt(corrupted_cipher)
    
    # 5.Đếm block lỗi với chế độ mã hóa tương ứng
    error_blocks = count_corrupted_blocks(plaintext, decrypted_text)

    print(f"[{mode}] Số block bản rõ bị hỏng: {error_blocks}")

def main():
    modes = ['ECB', 'CBC', 'CFB', 'OFB']
    for mode in modes:
        simulate_error(mode)
