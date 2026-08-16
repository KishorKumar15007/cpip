from backend.security.jwt import (
    create_access_token,
    verify_access_token,
)


token = create_access_token(42)

print("Token:")
print(token)

print("\nDecoded user ID:")
print(verify_access_token(token))


print("\nTesting invalid token:")
try:
    verify_access_token(token + "garbage")
except ValueError as e:
    print(e)
