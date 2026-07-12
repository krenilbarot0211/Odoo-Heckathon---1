from app.utils.auth import create_access_token, decode_access_token, get_role_permissions


def test_create_access_token_contains_role_and_email() -> None:
    token = create_access_token({"sub": "alex@example.com", "role": "administrator"})

    payload = decode_access_token(token)

    assert payload["sub"] == "alex@example.com"
    assert payload["role"] == "administrator"


def test_employee_role_has_restricted_permissions() -> None:
    permissions = get_role_permissions("employee")

    assert "publish_policy" not in permissions
    assert "submit_csr" in permissions
