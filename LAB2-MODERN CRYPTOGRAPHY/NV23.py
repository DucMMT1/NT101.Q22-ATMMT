from Crypto.Cipher import AES
import binascii

def count_bit_difference(bin1, bin2):
    # Đếm số bit khác nhau giữa 2 chuỗi nhị phân
    count = 0
    for b1, b2 in zip(bin1, bin2):
        if b1 != b2:
            count += 1
    return count

# Khởi tạo
key = b'1234567890123456'
cipher = AES.new(key, AES.MODE_ECB)

# Bản rõ 1 và Bản rõ 2 (chỉ khác nhau 1 ký tự cuối)
p1 = b'UIT_LAB_02_ABCDE' # 16 bytes
# Thay đổi chữ 'E' thành 'F' (thay đổi ít nhất 1 bit)
p2 = b'UIT_LAB_02_ABCDF' 

# Mã hóa
c1 = cipher.encrypt(p1)
c2 = cipher.encrypt(p2)

# Chuyển sang nhị phân để so sánh bit
bin1 = bin(int.from_bytes(c1, byteorder='big'))[2:].zfill(128)
bin2 = bin(int.from_bytes(c2, byteorder='big'))[2:].zfill(128)

# Tính toán
diff = count_bit_difference(bin1, bin2)
percentage = (diff / 128) * 100

print(f"Bản mã 1 (Hex): {c1.hex()}")
print(f"Bản mã 2 (Hex): {c2.hex()}")
print(f"Số bit khác nhau: {diff}/128")
print(f"Tỷ lệ thay đổi: {percentage:.2f}%")