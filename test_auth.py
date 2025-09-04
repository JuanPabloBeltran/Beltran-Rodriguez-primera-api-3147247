# test_auth.py
from auth import hash_password, verify_password, create_access_token, verify_token

def test_password_hashing():
    password = "mi_password_123"
    hashed = hash_password(password)
    print(f"Password original: {password}")
    print(f"Password hasheado: {hashed}")
    print(f"Password válido: {verify_password(password, hashed)}")
    print(f"Password incorrecto válido: {verify_password('otra', hashed)}")

def test_jwt_tokens():
    username = "juan123"
    token = create_access_token(username)
    print(f"Token creado: {token}")
    print(f"Username desde token: {verify_token(token)}")

if __name__ == "__main__":
    print("=== Test Password Hashing ===")
    test_password_hashing()
    print("\n=== Test JWT Tokens ===")
    test_jwt_tokens()
