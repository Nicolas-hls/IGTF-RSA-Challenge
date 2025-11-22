import sys

# --- CHALLENGE DATA ---
n = 162130897690355076680035390480057191266747082890320795180733814974920583723516800690727869351625939708165448030370049036461677303089504845016519686500699785679210605076702581294721764427530796902777125798705104462106443492149716927793245657774084209397383996163343777341661424803612681065834671874182217175489
e = 32
ct = 32275354532229624142969996979028002274979941770251135286963394869503485084445918327788820065726654488876070313219423388513961293299927597382670459924044672976727774200965357075447487200064018412908379336169065292070466774983422990727764213662528425233856857003066844483589029255171450400573476857048928778350

# --- MATH TOOLS ---
def tonelli_shanks(n_val, p):
    """ Finds x such that x^2 = n_val (mod p) """
    # 1. Check Legendre Symbol (Does a root exist?)
    if pow(n_val, (p - 1) // 2, p) != 1:
        return []
    
    # 2. Simple case: p = 3 mod 4
    if p % 4 == 3:
        x = pow(n_val, (p + 1) // 4, p)
        return [x, p - x] 
    
    # 3. Complex case: Full Tonelli-Shanks
    s = p - 1
    r = 0
    while s % 2 == 0:
        s //= 2
        r += 1
    
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
        
    c = pow(z, s, p)
    x = pow(n_val, (s + 1) // 2, p)
    t = pow(n_val, s, p)
    m = r
    
    while t != 1:
        if t == 0: return [0]
        i = 0
        temp = t
        while temp != 1:
            temp = pow(temp, 2, p)
            i += 1
        
        b = c
        for _ in range(m - i - 1):
            b = pow(b, 2, p)
            
        m = i
        c = pow(b, 2, p)
        t = (t * c) % p
        x = (x * b) % p
        
    return [x, p - x]

# --- SOLVING ---
print(f"[*] Decrypting...")
print(f"[*] e = {e} (2^5), so we loop 5 times.")

candidates = [ct]

# MAIN LOOP
for i in range(5):
    print(f"[*] Step {i+1}/5: Calculating roots...")
    next_gen = []
    
    for val in candidates:
        roots = tonelli_shanks(val, n)
        next_gen.extend(roots)
    
    # Remove duplicates
    candidates = list(set(next_gen))
    # Number of candidates (2, 4, 8...)
    print(f"    -> {len(candidates)} potential candidates found.")

# --- FLAG SEARCH ---
print("-" * 40)
print("[*] Filtering for readable text...")

found = False
for m in candidates:
    try:
        length = (m.bit_length() + 7) // 8
        msg = m.to_bytes(length, 'big')
        
        if b"IGTF{" in msg:
            print(f"\n[VICTORY !!!] Flag found:\n")
            print(f"Result: {msg.decode()}")
            print("\n")
            found = True
            break
    except:
        continue

if not found:
    print("[-] No flag found. Check the data.")
