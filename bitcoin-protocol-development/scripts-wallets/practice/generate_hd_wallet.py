from os import urandom
from hashlib import sha256, sha512, pbkdf2_hmac
from mnemonic import Mnemonic
from bip32utils import BIP32Key
import hmac
import struct
import ecdsa
from ecdsa.curves import SECP256k1
from ecdsa.ecdsa import int_to_string, string_to_int
from ecdsa.numbertheory import square_root_mod_prime as sqrt_mod

WORDLIST = Mnemonic('english').wordlist
ENTROPY_LENGTH = 128
ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
FIELD_ORDER = SECP256k1.curve.p()


def encode_base58(x):
    p, acc = 1, 0
    for c in reversed(x):
        acc += p * c
        p = p << 8

    x_base58 = ""
    while acc:
        acc, idx = divmod(acc, 58)
        x_base58 = ALPHABET[idx: idx + 1] + x_base58

    return x_base58


# entropy:
#   generate 128 bits of entropy
entropy = urandom(ENTROPY_LENGTH // 8)
print("entropy:", entropy)
print("entropy_hex:", entropy.hex())
# entropy_binary:
#   convert entropy bytes to integer in big endian order
#   convert big endian integer to bits
#   drop '0b' from front
#   pad front with 0s until length of resulting string = full entropy length in bits
entropy_binary = bin(int.from_bytes(entropy, byteorder="big"))[
    2:].zfill(len(entropy) * 8)
print("entropy_binary:", entropy_binary)

# entropy_hash_256:
#   generate 256 bit hash using sha256
#   digest into hex format
entropy_hash_256 = sha256(entropy).hexdigest()
print("entropy_hash:", entropy_hash_256)
# entropy_hash_256_binary:
#   convert entropy_hash_256 from hex to integer then integer to bits
#   drop '0b' from front of bits
#   pad front with 0s until length of resulting bits = 256
entropy_hash_256_binary = bin(int(entropy_hash_256, 16))[2:].zfill(256)
print("entropy_hash_256_binary:", entropy_hash_256_binary)

# checksum_length:
#   determine the checksum length based on full entropy length in bits
#   entropy = 128, checksum length = 4
#   entropy = 256, checksum length = 8
checksum_length = len(entropy) * 8 // 32
# checksum:
#   get checksum_length bytes from start of entropy hash bits
checksum = entropy_hash_256_binary[:checksum_length]
# entropy_checksum:
#   append binary checksum to end of entropy bits
entropy_checksum_binary = entropy_binary + checksum
print("entropy_checksum_binary:", entropy_checksum_binary)

# entropy_checksum_binary_segments:
#   split the entropy bits + checksum into a list of 11 bit segments
#   entropy = 128, checksum length = 4, entropy_checksum = 132, 11_bit_segments = 12
#   entropy = 256, checksum length = 8, entropy_checksum = 264, 11_bit_segments = 24
mnemonic_words = []
for i in range(len(entropy_checksum_binary) // 11):
    word_index = int(entropy_checksum_binary[i * 11: (i + 1) * 11], 2)
    mnemonic_words.append(WORDLIST[word_index])

mnemonic_phrase = " ".join(mnemonic_words)
print("mnemonic:", mnemonic_phrase, '\n')

passphrase = "mnemonic" + ""
mnemonic_phrase_bytes = mnemonic_phrase.encode("utf-8")
passphrase_bytes = passphrase.encode("utf-8")
PBKDF2_ROUNDS = 2048
seed_hash_512 = pbkdf2_hmac(
    "sha512", mnemonic_phrase_bytes, passphrase_bytes, PBKDF2_ROUNDS)
print("seed_hash_512:", seed_hash_512)

master_extended_private_key = hmac.new(
    b"Bitcoin seed", seed_hash_512, digestmod=sha512).digest()
master_private_key = master_extended_private_key[32:]
master_chain_code = b"\x00" + master_extended_private_key[:32]

xprv = b"\x04\x88\xad\xe4"
depth_pfp_childnum = b"\x00" * 9
xprv += depth_pfp_childnum
xprv += master_private_key
xprv += master_chain_code
print("xprv_0:", xprv)

xprv_checksum = sha256(sha256(xprv).digest()).digest()[:4]
print("xprv_checksum:", xprv_checksum)

# Append 4 bytes of checksum
xprv = encode_base58(xprv + xprv_checksum)

# TODO: learn how to generate xpub from xpriv from scratch
bip32_xpriv = BIP32Key.fromExtendedKey(xprv)
master_extended_public_key = bip32_xpriv.PublicKey()
xpub = bip32_xpriv.ExtendedKey(private=False)

print("Master Private Key:", master_extended_private_key.hex())
print("Master Public Key: ", master_extended_public_key.hex())
print("Master Chain Code: ", master_chain_code.hex(), '\n')

print("Extended Private Key:", xprv)
print("Extended Public Key: ", xpub)
