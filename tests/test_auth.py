from tests.conftest import register_and_login

def test_signup_and_login_flow(client):
    r = client.post("/signup", data={"email": "u@ex.com", "username": "user", "password": "pw"}, follow_redirects=True)
    assert r.status_code == 200
    assert b"@user" in r.data

    # logout then login
    client.get("/logout")
    r2 = client.post("/login", data={"email": "u@ex.com", "password": "pw"}, follow_redirects=True)
    assert b"@user" in r2.data
