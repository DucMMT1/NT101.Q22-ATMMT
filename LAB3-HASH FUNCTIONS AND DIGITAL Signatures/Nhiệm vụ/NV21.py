import math
import base64

def extended_gcd(a: int, b: int):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    return gcd, y1 - (b // a) * x1, x1


def mod_inverse(e: int, phi: int) -> int:
    gcd, x, _ = extended_gcd(e % phi, phi)
    if gcd != 1:
        raise ValueError(f"Không tồn tại nghịch đảo: gcd({e}, {phi}) = {gcd}")
    return x % phi


def generate_rsa_keys(p: int, q: int, e: int):
    n = p * q
    phi_n = (p - 1) * (q - 1)
    assert math.gcd(e, phi_n) == 1, \
        f"e={e} không nguyên tố cùng nhau với φ(n)={phi_n}"
    d = mod_inverse(e, phi_n)
    return (e, n), (d, n), phi_n

def rsa_enc_conf(M: int, PU: tuple) -> int:
    e, n = PU
    return pow(M, e, n)

def rsa_dec_conf(C: int, PR: tuple) -> int:
    d, n = PR
    return pow(C, d, n)

def rsa_enc_auth(M: int, PR: tuple) -> int:
    d, n = PR
    return pow(M, d, n)

def rsa_dec_auth(C: int, PU: tuple) -> int:
    e, n = PU
    return pow(C, e, n)

def _pt_block(n: int) -> int:
    return max(1, (n.bit_length() - 1) // 8)

def _ct_block(n: int) -> int:
    return (n.bit_length() + 7) // 8


def enc_str(msg: str, exp: int, n: int) -> bytes:
    pt = _pt_block(n)
    ct = _ct_block(n)
    raw = msg.encode('utf-8')
    orig_len = len(raw)

    pad = (-len(raw)) % pt
    raw_padded = raw + b'\x00' * pad

    out = orig_len.to_bytes(2, 'big')
    for i in range(0, len(raw_padded), pt):
        m_int = int.from_bytes(raw_padded[i:i + pt], 'big')
        c_int = pow(m_int, exp, n)
        out += c_int.to_bytes(ct, 'big')
    return out


def dec_str(ciph: bytes, exp: int, n: int) -> str:
    orig_len = int.from_bytes(ciph[:2], 'big')
    ciph = ciph[2:]
    pt = _pt_block(n)
    ct = _ct_block(n)
    out = b''
    for i in range(0, len(ciph), ct):
        c_int = int.from_bytes(ciph[i:i + ct], 'big')
        m_int = pow(c_int, exp, n)
        out += m_int.to_bytes(pt, 'big')
    return out[:orig_len].decode('utf-8')

def try_decrypt(ciph: bytes, keys: list):
    for label, PU, PR in keys:
        n = PU[1]
        ct = _ct_block(n)
        for mode, exp in [("Bảo mật (dùng PR)", PR[0]),
                          ("Xác thực (dùng PU)", PU[0])]:
            # Thử với header 2 byte (định dạng enc_str)
            for has_header in [True, False]:
                try:
                    data = ciph[2:] if has_header else ciph
                    if has_header:
                        orig_len = int.from_bytes(ciph[:2], 'big')
                        if orig_len > 10000 or orig_len == 0:
                            continue
                    if len(data) % ct != 0:
                        continue
                    pt = _pt_block(n)
                    out = b''
                    for i in range(0, len(data), ct):
                        c_int = int.from_bytes(data[i:i + ct], 'big')
                        m_int = pow(c_int, exp, n)
                        out += m_int.to_bytes(pt, 'big')
                    if has_header:
                        raw = out[:orig_len]
                    else:
                        raw = out.rstrip(b'\x00')
                    text = raw.decode('utf-8')
                    if text.isprintable() and len(text.strip()) > 0:
                        return label, mode, text
                except Exception:
                    pass
    return None, None, None

def main():
    print("1. Khóa 1: p1=11, q2=17, e3=7 (hệ thập phân)")
    p1, q1, e1 = 11, 17, 7
    PU1, PR1, phi1 = generate_rsa_keys(p1, q1, e1)
    print(f" n = p × q = {p1} × {q1} = {PU1[1]}")
    print(f" φ(n) = (p-1)(q-1) = {p1-1}×{q1-1} = {phi1}")
    print(f" e = {e1}  →  gcd(e, φ(n)) = {math.gcd(e1, phi1)}")
    print(f" d = {PR1[0]}  [kiểm tra: {e1} × {PR1[0]} mod {phi1} = {(e1*PR1[0])%phi1}]")
    print(f"\n  Khóa công khai: PU1 = (e={PU1[0]},  n={PU1[1]})")
    print(f"  Khóa riêng tư: PR1 = (d={PR1[0]}, n={PR1[1]})\n")

    print("   Khóa 2: p2, q2 thập phân, e2=17")
    p2 = 20079993872842322116151219
    q2 = 676717145751736242170789
    e2 = 17
    PU2, PR2, phi2 = generate_rsa_keys(p2, q2, e2)
    print(f" p = {p2}")
    print(f" q = {q2}")
    print(f" n = {PU2[1]}")
    print(f" φ(n) = {phi2}")
    print(f" e = {e2}  →  gcd(e, φ(n)) = {math.gcd(e2, phi2)}")
    print(f" d = {PR2[0]}")
    print(f"\n  Khóa công khai: PU2 = (e={PU2[0]}, n={PU2[1]})")
    print(f"  Khóa riêng tư: PR2 = (d={PR2[0]}, n={PR2[1]})\n")

    print("   Khóa 3: p3, q3, e3 thập lục phân")
    p3 = int("F7E75FDC469067FFDC4E847C51F452DF", 16)
    q3 = int("E85CED54AF57E53E092113E62F436F4F", 16)
    e3 = int("0D88C3", 16)
    PU3, PR3, phi3 = generate_rsa_keys(p3, q3, e3)
    print(f" p (hex) = F7E75FDC469067FFDC4E847C51F452DF")
    print(f" p (dec) = {p3}")
    print(f" q (hex) = E85CED54AF57E53E092113E62F436F4F")
    print(f" q (dec) = {q3}")
    print(f" e (hex) = 0D88C3  →  e (dec) = {e3}")
    print(f" n = {PU3[1]}")
    print(f" φ(n) = {phi3}")
    print(f" d = {PR3[0]}")
    print(f"\n  Khóa công khai: PU3 = (e={PU3[0]}, n={PU3[1]})")
    print(f"  Khóa riêng tư: PR3 = (d={PR3[0]}, n={PR3[1]})\n")

    print("2. Mã hóa / giải mã M=5 với bộ khóa 1")
    M = 5
    print(f"  Bản rõ M = {M}")

    C_s = rsa_enc_conf(M, PU1)
    M_s = rsa_dec_conf(C_s, PR1)
    print(f"\n  --Bảo mật (Encryption for Confidentiality)--")
    print(f"    Mã hóa  : C = M^e mod n = {M}^{PU1[0]} mod {PU1[1]} = {C_s}")
    print(f"    Giải mã : M = C^d mod n = {C_s}^{PR1[0]} mod {PR1[1]} = {M_s}  "
          f"{' (Khớp)' if M_s == M else ' (Sai)'}")

    C_a = rsa_enc_auth(M, PR1)
    M_a = rsa_dec_auth(C_a, PU1)
    print(f"\n  --Xác thực (Encryption for Authentication)--")
    print(f"    Mã hóa  : C = M^d mod n = {M}^{PR1[0]} mod {PR1[1]} = {C_a}")
    print(f"    Giải mã : M = C^e mod n = {C_a}^{PU1[0]} mod {PU1[1]} = {M_a}  "
          f"{' (Khớp)' if M_a == M else ' (Sai)'}")

    print("3. Mã hóa chuỗi 'The University of Information Technology'")
    message = "The University of Information Technology"
    print(f"  Thông điệp: \"{message}\"  ({len(message.encode())} bytes)\n")

    for label, PU, PR in [("Bộ khóa 1", PU1, PR1),
                           ("Bộ khóa 2", PU2, PR2),
                           ("Bộ khóa 3", PU3, PR3)]:
        n = PU[1]
        pt_b = _pt_block(n)
        ct_b = _ct_block(n)
        print(f"  ── {label}  (n = {n.bit_length()} bit | pt_block = {pt_b} B | ct_block = {ct_b} B) ──")

        ct_s = enc_str(message, PU[0], n)
        b64_s = base64.b64encode(ct_s).decode()
        pt_s  = dec_str(ct_s, PR[0], n)
        ok_s = '✓' if pt_s == message else '✗'
        print(f"    [Bảo mật]  Base64 = {b64_s}")
        print(f"               Giải mã: \"{pt_s}\"  {ok_s}")

        ct_a = enc_str(message, PR[0], n)
        b64_a = base64.b64encode(ct_a).decode()
        pt_a  = dec_str(ct_a, PU[0], n)
        ok_a = '✓' if pt_a == message else '✗'
        print(f"    [Xác thực] Base64 = {b64_a}")
        print(f"               Giải mã: \"{pt_a}\"  {ok_a}\n")

    print("4. Tìm bản rõ của các bản mã cho sẵn")
    all_keys = [("Khóa 1", PU1, PR1),
                ("Khóa 2", PU2, PR2),
                ("Khóa 3", PU3, PR3)]

    ciphers = [
        ("Bản mã 1 (Base64)",
         base64.b64decode(
             "raUcesUlOkx/8ZhgodMoo0Uu18sC20yXlQFevSu7W/FDxIy0YRHMyX"
             "cHdD9PBvIT2aUft5fCQEGomiVVPv4I")),
        ("Bản mã 2 (Hex)",
         bytes.fromhex("C87F570FC4F699CEC24020C6F54221ABAB2CE0C3")),
        ("Bản mã 3 (Base64)",
         base64.b64decode(
             "Z2BUSkJcg0w4XEpgm0JcMExEQmBlVH6dYEpNTHpMHptMQ7NgTHlg"
             "QrNMQ2BKTQ==")),
        ("Bản mã 4 (Binary string)",
         int(
             "001010000001010011111111101101110010111011001010111011000110011"
             "110111111001111110110100011001111001100001001010001010100111101"
             "010100110011101110111011110101101100000100",
             2).to_bytes(21, 'big')),
    ]

    for name, ciph in ciphers:
        print(f"\n  {name}  ({len(ciph)} bytes)")
        label, mode, pt = try_decrypt(ciph, all_keys)
        if pt:
            print(f"  → Khóa   : {label}")
            print(f"  → Chế độ : {mode}")
            print(f"  → Bản rõ : \"{pt}\"")
        else:
            print("  → Không giải mã được với 3 bộ khóa đã cho.")
            print("    (Có thể bản mã thuộc một bộ khóa khác hoặc dùng "
                  "phương thức mã hóa khác biệt.)")

if __name__ == "__main__":
    main()