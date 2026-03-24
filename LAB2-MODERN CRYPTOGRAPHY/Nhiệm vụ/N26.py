import random

# 1. KIỂM TRA SỐ NGUYÊN TỐ (MILLER-RABIN)
"""
    Thuật toán kiểm tra tính nguyên tố Miller-Rabin (xác suất).
    - n: Số cần kiểm tra.
    - k: Số vòng lặp thử nghiệm 
"""
def is_prime_miller_rabin(n, k=5):
    if n <= 1: 
        return False
    if n <= 3: 
        return True
    if n % 2 == 0: 
        return False 

    r = n - 1
    d = 0
    while r % 2 == 0:
        d += 1
        r //= 2

    # Bắt đầu k vòng lặp thử nghiệm
    for _ in range(k):
        a = random.randint(2, n - 2) # Chọn ngẫu nhiên cơ số a trong khoảng [2, n-2]
        
        # Tính x = (a^r) mod n
        x = modular_exponentiation(a, r, n)
        
        if x == 1 or x == n - 1:
            continue # Nếu thỏa mãn, chuyển sang thử nghiệm a tiếp theo
            
        for _ in range(d - 1):
            # Tính tiếp x = (x^2) mod n
            x = modular_exponentiation(x, 2, n)
            if x == n - 1:
                break # Thỏa mãn, chuyển sang thử nghiệm a tiếp theo
        else:
            # Nếu vòng lặp trong (for _ in range(d-1)) chạy hết mà không break, n là hợp số
            return False
            
    # Nếu vượt qua toàn bộ k bài kiểm tra, xác suất rất cao n là số nguyên tố
    return True

#Tạo ra một số nguyên tố ngẫu nhiên có độ dài bit xác định.
def generate_n_bit_prime(bits):
    while True:
        # Sinh một số ngẫu nhiên có 'bits' bit
        num = random.getrandbits(bits)
        
        # Đảm bảo bit cao nhất là 1 (để đủ số bit) và bit thấp nhất là 1 (để là số lẻ)
        num |= (1 << bits - 1) | 1 
        
        if is_prime_miller_rabin(num):
            return num


# 2. ƯỚC CHUNG LỚN NHẤT (EUCLID)
"""
    Thuật toán Euclid tìm Ước chung lớn nhất.
    Nguyên lý: GCD(a, b) = GCD(b, a mod b).
"""
def gcd(a, b):
    while b != 0:
        # Cập nhật a bằng b, và b bằng phần dư của a chia b
        a, b = b, a % b
    return a


# 3. LŨY THỪA MODULO (SQUARE AND MULTIPLY)
"""
    Thuật toán Bình phương và Nhân (Square and Multiply).
    Dựa trên tính chất: (a * b) mod n = [(a mod n) * (b mod n)] mod n.
"""
def modular_exponentiation(a, x, p):
    result = 1
    a = a % p 
    
    while x > 0:
        # Nếu bit cuối cùng của x là 1 (nghĩa là x lẻ)
        if x % 2 == 1:
            result = (result * a) % p # Nhân cơ số a vào kết quả
            
        # Dịch phải x đi 1 bit (= chia 2)
        x //= 2
        
        a = (a * a) % p 
        
    return result

if __name__ == "__main__":
    print("--- 1. TẠO SỐ NGUYÊN TỐ ---")
    print(f"Prime 8-bit : {generate_n_bit_prime(8)}")
    print(f"Prime 16-bit: {generate_n_bit_prime(16)}")
    print(f"Prime 64-bit: {generate_n_bit_prime(64)}")

    print("\n TÌM 10 SỐ NGUYÊN TỐ LỚN NHẤT NHỎ HƠN MERSENNE THỨ 10 ")
    M10 = (1 << 89) - 1 
    primes_under_M10 = []
    
    # Bắt đầu kiểm tra ngược từ sát dưới M10
    num = M10 - 1
    while len(primes_under_M10) < 10:
        if is_prime_miller_rabin(num):
            primes_under_M10.append(num)
        num -= 2 # Giảm đi 2 để chỉ kiểm tra số lẻ 
        
    print(f"Số Mersenne thứ 10: {M10}")
    print("10 số nguyên tố lớn nhất ngay dưới nó là:")
    for i, p in enumerate(primes_under_M10, 1):
        print(f"{i}. {p}")

    print("\n  2. TÍNH GCD CỦA 2 SỐ LỚN ")
    # Tự sinh 2 số lớn (128-bit) để test nghiệm
    num1 = generate_n_bit_prime(128) * 17
    num2 = generate_n_bit_prime(128) * 23
    print(f"Num 1: {num1}")
    print(f"Num 2: {num2}")
    print(f"GCD  : {gcd(num1, num2)}")

    print("\n 3. TÍNH LŨY THỪA MODULO ")
    # Yêu cầu: Tính 7^40 mod 19 
    a, x, p = 7, 40, 19
    res = modular_exponentiation(a, x, p)
    print(f"{a}^{x} mod {p} = {res}")