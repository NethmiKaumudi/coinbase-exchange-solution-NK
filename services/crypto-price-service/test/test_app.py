
import pytest
from app import app


@pytest.fixture
def client():
    app.testing = True
    yield app.test_client()


def test_get_crypto_prices(client):
    response = client.get('/crypto-prices')
    assert response.status_code == 200
    assert 'BTC' in response.get_json()
    assert 'ETH' in response.get_json()
    assert 'LTC' in response.get_json()
