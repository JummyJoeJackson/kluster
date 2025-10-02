from tests.conftest import register_and_login

def test_add_and_list_items(client):
    register_and_login(client)
    r = client.post("/collection/add", data={
        "name":"Omega Speedmaster",
        "description":"Moonwatch",
        "category":"Watches",
        "estimated_value":"5200.50"
    }, follow_redirects=True)
    assert r.status_code == 200
    assert b"Omega Speedmaster" in r.data
    assert b"Total value" in r.data
