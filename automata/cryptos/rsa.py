def encrypt(message, pub_key): 
    #RSA encryption protocol according to PKCS#1 OAEP 
    cipher = PKCS1_OAEP.new(pub_key) 
    return cipher.encrypt(message) 

def decrypt(ciphertext, priv_key): 
    #RSA encryption protocol according to PKCS#1 OAEP 
    cipher = PKCS1_OAEP.new(priv_key) 
    return cipher.decrypt(ciphertext) 

def sign(message, priv_key, hashAlg="SHA-256"): 
    global hash 
    hash = hashAlg 
    signer = PKCS1_v1_5.new(priv_key) 
    if (hash == "SHA-512"): 
     digest = SHA512.new() 
    elif (hash == "SHA-384"): 
     digest = SHA384.new() 
    elif (hash == "SHA-256"): 
     digest = SHA256.new() 
    elif (hash == "SHA-1"): 
     digest = SHA.new() 
    else: 
     digest = MD5.new() 
    digest.update(message) 
    return signer.sign(digest) 

def verify(message, signature, pub_key): 
    signer = PKCS1_v1_5.new(pub_key) 
    if (hash == "SHA-512"): 
     digest = SHA512.new() 
    elif (hash == "SHA-384"): 
     digest = SHA384.new() 
    elif (hash == "SHA-256"): 
     digest = SHA256.new() 
    elif (hash == "SHA-1"): 
     digest = SHA.new() 
    else: 
     digest = MD5.new() 
    digest.update(message) 
    return signer.verify(digest, signature) 