import pytest
from app import app


@pytest.fixture
def client():
    app.testing = True
    yield app.test_client()


def test_get_accounts(client):
    response = client.get('/accounts')
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_account(client):
    account_data = {'id': 1, 'name': 'John Doe'}
    response = client.post('/accounts', json=account_data)
    assert response.status_code == 201
    assert response.get_json() == account_data
