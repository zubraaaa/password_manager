import pytest
import csv
from pass_mng import (
    encrypt_password,
    decrypt_password,
    add_password,
    load_passwords_from_file,
    get_password,
    passwords  # глобальний список
)

def test_encrypt_and_decrypt_password():
    original = "my_secret_password"
    encrypted = encrypt_password(original)
    decrypted = decrypt_password(encrypted)
    assert decrypted == original

def test_add_password_does_not_save_file():
    passwords.clear()
    entry = add_password("example.com", "user1", "pass123", save_to_file=False)
    assert entry["website"] == "example.com"
    assert decrypt_password(entry["password"]) == "pass123"

def test_add_and_load_passwords_from_csv(tmp_path):
    passwords.clear()
    csv_path = tmp_path / "passwords.csv"

    # Додаємо 1 пароль у тимчасовий CSV
    entry = add_password("site.com", "admin", "admin123", save_to_file=False)
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([entry["website"], entry["username"], entry["password"].decode()])

    # Завантажуємо з цього CSV
    load_passwords_from_file(str(csv_path))

    assert len(passwords) == 1
    loaded = passwords[0]
    assert loaded["website"] == "site.com"
    assert decrypt_password(loaded["password"]) == "admin123"

def test_get_password_returns_correct_entry():
    passwords.clear()
    add_password("github.com", "gituser", "gh_pass", save_to_file=False)

    result = get_password("github.com")
    assert result is not None
    assert result["website"] == "github.com"
    assert result["username"] == "gituser"
    assert result["password"] == "gh_pass"

def test_get_password_returns_none_for_missing_site():
    passwords.clear()
    result = get_password("nosite.com")
    assert result is None
