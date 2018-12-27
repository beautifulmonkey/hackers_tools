# -*- coding: utf-8 -*-
"""
	生成新的公钥和私钥
"""
import rsa

NBITS = 1000

(PublicKey, PrivateKey) = rsa.newkeys(NBITS)

with open("PublicKey.pem", "w") as f:
	f.write(PublicKey.save_pkcs1())

with open("PrivateKey.pem", "w") as f:
	f.write(PrivateKey.save_pkcs1())
