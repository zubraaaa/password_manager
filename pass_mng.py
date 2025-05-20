import csv
from cryptography.fernet import Fernet

passwords = []
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_password(password):
    return cipher_suite.encrypt(password.encode())

def decrypt_password(encrypted_password):
    return cipher_suite.decrypt(encrypted_password).decode()

def add_password(website, username, password, save_to_file=True):
    encrypted_password = encrypt_password(password)
    entry = {
        "website": website,
        "username": username,
        "password": encrypted_password
    }
    passwords.append(entry)
    
    if save_to_file:
        with open('passwords.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([website, username, encrypted_password])
    
    return entry

def load_passwords_from_file(filename='passwords.csv'):
    passwords.clear()
    try:
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                passwords.append({
                    "website": row[0],
                    "username": row[1],
                    "password": row[2].encode()  # Convert string to bytes
                })
    except FileNotFoundError:
        pass  # файл ще не існує

def get_password(website):
    for entry in passwords:
        if entry["website"] == website:
            decrypted = decrypt_password(entry["password"])
            return {
                "website": website,
                "username": entry["username"],
                "password": decrypted
            }
    return None
