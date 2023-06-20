from werkzeug.security import generate_password_hash

passwords = ["passa", "passm1", "passm2", "passc1", "passc2"]

for password in passwords:
    password_hash = generate_password_hash(password)
    print(f"Password: {password}\tHash: {password_hash}")
