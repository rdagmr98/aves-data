import json, base64

KEY = b'd694b158908b35cc05cf4f4b39ab0e3c'[:32]
IV = b'\x00' * 16

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def encrypt(plaintext):
    if not plaintext:
        return plaintext
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    ct = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return 'ENC:' + base64.b64encode(ct).decode()

def migrate_users():
    with open('db/users.json', encoding='utf-8') as f:
        users = json.load(f)
    for u in users:
        for field in ['nome', 'cognome', 'email', 'numero_licenza', 'username']:
            if u.get(field) and not str(u[field]).startswith('ENC:'):
                u[field] = encrypt(str(u[field]))
    with open('db/users.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)
    print(f'Migrated {len(users)} users')

migrate_users()
