from tests.conftest import register_and_login

def test_search_users_and_items(client):
    register_and_login(client, email="a@a.com", username="alice")
    # add item
    client.post("/collection/add", data={"name": "Rolex Submariner", "estimated_value":"10000", "description":"", "category":"Watches"})
    # a second user
    client.get("/logout")
    register_and_login(client, email="b@b.com", username="bob")

    r = client.get("/search?q=Rolex")
    assert b"Rolex Submariner" in r.data

    r2 = client.get("/search?q=ali")
    assert b"@alice" in r2.data
