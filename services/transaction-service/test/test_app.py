import pytest
from app import app


@pytest.fixture
def client():
    app.testing = True
    yield app.test_client()


def test_get_transactions(client):
    response = client.get('/transactions')
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_transaction(client):
    transaction_data = {'id': 1, 'amount': 100, 'currency': 'USD'}
    response = client.post('/transactions', json=transaction_data)
    assert response.status_code == 201
    assert response.get_json() == transaction_data
