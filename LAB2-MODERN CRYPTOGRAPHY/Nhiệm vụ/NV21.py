#Thuc hien XOR giua right va subkey (R,K)
def F(right, subkey):
    return (right ^ subkey) & 0x0F

def feistel_round(L_in, R_in, subkey):
    #LE_i = RE_{i-1} 
    L_out = R_in 
    #RE_i = LE_{i-1} XOR F(RE_{i-1}, K_i)
    R_out = L_in ^ F(R_in, subkey)
    return L_out, R_out


 
def track_avalanche(msg, key):
    # Tách bản rõ thành 2 nửa L và R (mỗi nửa 4 bit)
    L, R = (msg >> 4) & 0x0F, msg & 0x0F

    # Tạo các subkeys
    subkeys = [key & 0x0F, (key >> 4) & 0x0F, (key + 1) & 0x0F, (key + 2) & 0x0F]

    print(f"Khởi tạo: L={format(L, '04b')}, R={format(R, '04b')}")

    for i in range(4):
        L, R = feistel_round(L, R, subkeys[i])
        print(f"Vong {i+1}: L={format(L, f'0{4}b')}, R={format(R, f'0{4}b')}")
    return (L << 4) | R
    
# Chay thu voi 2 ban ro khac nhau 1 bit
print("--- Ma hoa M1 ---")
track_avalanche(0xAB, 0x12)
print("--- Ma hoa M2 ---")
track_avalanche(0xAC, 0x12)