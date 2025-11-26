import pytest
import httpx

BASE_URL = "http://127.0.0.1:8000/v1/accounts"

test_data = {
    "iban": None,
    "initial_name": "test_name",
    "initial_email": "test.openapi@example.com",
    "initial_subscription": "Free"
    }

@pytest.mark.asyncio
@pytest.mark.dependency(name="create_account")
async def test_create_account():
    """
    Test POST /v1/accounts/ — Create new account
    """
    async with httpx.AsyncClient() as client:
        payload = {
            "name": test_data["initial_name"],
            "email": test_data["initial_email"],
            "subscription": test_data["initial_subscription"]
            }
        response = await client.post(f"{BASE_URL}/", json=payload)
        
        assert response.status_code == 201, "Create account fail"
        response_json = response.json()
        
        assert "iban" in response_json
        assert response_json["name"] == test_data["initial_name"]
        assert response_json["email"] == test_data["initial_email"]
        assert response_json["subscription"] == test_data["initial_subscription"]
        assert response_json["isBlocked"] is False
        assert "balance" in response_json
        
        test_data["iban"] = response_json["iban"]


@pytest.mark.asyncio
async def test_create_account_missing_param():
    """
    Test POST /v1/accounts/ — Post missing param
    """
    async with httpx.AsyncClient() as client:
        payload = {
            "email": "fail@example.com",
            "subscription": "Free"
            }
        response = await client.post(f"{BASE_URL}/", json=payload)
        assert response.status_code in [400]


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["create_account"])
async def test_get_account():
    """
    Test GET /v1/accounts/<iban> — Get created account
    """
    assert test_data["iban"] is not None, "IBAN was not created"
    iban = test_data["iban"]
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/{iban}")
        
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["iban"] == iban
        assert response_json["name"] == test_data["initial_name"]


@pytest.mark.asyncio
async def test_get_account_not_found_invalid_IBAN():
    """
    Test GET /v1/accounts/<iban> — Get non-existent account
    """
    async with httpx.AsyncClient() as client:
        valid_iban = "ES6915574722004050030844"
        response = await client.get(f"{BASE_URL}/{valid_iban}")
        assert response.status_code == 400
        
@pytest.mark.asyncio
async def test_get_account_not_found():
    """
    Test GET /v1/accounts/<iban> — Get non-existent account
    """
    async with httpx.AsyncClient() as client:
        valid_iban = "ES6915574722004050030834"
        response = await client.get(f"{BASE_URL}/{valid_iban}")
        assert response.status_code == 404


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["create_account"])
async def test_update_account_email():
    """
    Test PATCH /v1/accounts/<iban> — Update only email (one param)
    """
    iban = test_data["iban"]
    new_email = "updated.email@example.com"
    
    async with httpx.AsyncClient() as client:
        payload = {"email": new_email}
        response = await client.patch(f"{BASE_URL}/{iban}", json=payload)
        
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["email"] == new_email
        
        assert response_json["name"] == test_data["initial_name"]


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["create_account"])
async def test_update_account_balance_multiple(request):
    """
    Test PATCH /v1/accounts/operation/<iban> — Update balance.
    """
    iban = test_data["iban"]
    
    async with httpx.AsyncClient() as client:
        get_res = await client.get(f"{BASE_URL}/{iban}")
        assert get_res.status_code == 200
        current_balance = get_res.json()["balance"]
        
        
        balance_to_add_1 = 100
        payload_1 = {"balance": balance_to_add_1}
        response_1 = await client.patch(f"{BASE_URL}/operation/{iban}", json=payload_1)
        
        assert response_1.status_code == 200
        expected_balance_1 = current_balance + balance_to_add_1
        assert response_1.json()["balance"] == expected_balance_1
        
        
        balance_to_add_2 = 50
        payload_2 = {"balance": balance_to_add_2}
        response_2 = await client.patch(f"{BASE_URL}/operation/{iban}", json=payload_2)
        
        assert response_2.status_code == 200
        expected_balance_2 = expected_balance_1 + balance_to_add_2
        assert response_2.json()["balance"] == expected_balance_2


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["create_account"])
async def test_update_account_balance_insufficient(request):
    """
    Test PATCH /v1/accounts/operation/<iban> — Unsufficient balance operation.
    """
    iban = test_data["iban"]
    
    async with httpx.AsyncClient() as client:
        get_res = await client.get(f"{BASE_URL}/{iban}")
        assert get_res.status_code == 200
        current_balance = get_res.json()["balance"]
        
        
        balance_to_withdraw = current_balance + 1000
        payload = {"balance": -balance_to_withdraw}
        
        response = await client.patch(f"{BASE_URL}/operation/{iban}", json=payload)
        assert response.status_code == 403
        
        
        get_res_after = await client.get(f"{BASE_URL}/{iban}")
        assert get_res_after.status_code == 200
        balance_after = get_res_after.json()["balance"]
        
        assert balance_after == current_balance


@pytest.mark.asyncio
async def test_update_account_balance_not_found():
    """
    Test PATCH /v1/accounts/operation/<iban> — Update balance of non-existent account.
    """
    async with httpx.AsyncClient() as client:
        payload = {"balance": 100}
        valid_iban = "ES6915574722004050030834"
        response = await client.patch(f"{BASE_URL}/operation/{valid_iban}", json=payload)
        assert response.status_code == 404


@pytest.mark.asyncio
@pytest.mark.dependency(name="block_account", depends=["create_account"])
async def test_block_account():
    """
    Test PATCH /v1/accounts/<iban>/block — Block account
    """
    iban = test_data["iban"]
    async with httpx.AsyncClient() as client:
        response = await client.patch(f"{BASE_URL}/{iban}/block")
        assert response.status_code == 204
        
        get_res = await client.get(f"{BASE_URL}/{iban}")
        assert get_res.status_code == 200
        assert get_res.json()["isBlocked"] is True


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["block_account"])
async def test_unblock_account():
    """
    Test PATCH /v1/accounts/<iban>/unblock — Unblock account
    """
    iban = test_data["iban"]
    async with httpx.AsyncClient() as client:
        response = await client.patch(f"{BASE_URL}/{iban}/unblock")
        
        assert response.status_code == 204
        
        get_res = await client.get(f"{BASE_URL}/{iban}")
        assert get_res.status_code == 200
        assert get_res.json()["isBlocked"] is False


@pytest.mark.asyncio
async def test_delete_account_not_found():
    """
    Test DELETE /v1/accounts/<iban> — Delete non-existent account
    """
    async with httpx.AsyncClient() as client:
        valid_iban = "ES6915574722004050030834"
        response = await client.delete(f"{BASE_URL}/{valid_iban}")
        assert response.status_code == 404


@pytest.mark.asyncio
@pytest.mark.dependency(name="delete_account", depends=["create_account"])
async def test_delete_account():
    """
    Test DELETE /v1/accounts/<iban> — Delete account
    """
    iban = test_data["iban"]
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{BASE_URL}/{iban}")
        assert response.status_code == 204


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["delete_account"])
async def test_verify_account_deleted():
    """
    Test GET /v1/accounts/<iban> — Verify deletion of account.
    """
    iban = test_data["iban"]
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/{iban}")
        assert response.status_code == 404