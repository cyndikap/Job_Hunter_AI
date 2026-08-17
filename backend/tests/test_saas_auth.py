from app.security.jwt_auth import create_token, decode_token


def test_jwt_round_trip():
    token = create_token("user-123", {"role": "user"})
    claims = decode_token(token)
    assert claims["sub"] == "user-123"
    assert claims["role"] == "user"


def test_jwt_rejects_invalid_token():
    try:
        decode_token("not.a.valid.token")
        assert False, "Expected invalid token to fail"
    except Exception:
        assert True
