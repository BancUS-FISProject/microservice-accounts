import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

from src.service_name.models.Accounts import AccountBase, AccountUpdate, AccountUpdatebalance, AccountView
from src.service_name.db.AccountsRepository import AccountRepository


pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
def mock_collection():
    collection = MagicMock()
    collection.insert_one = AsyncMock()
    collection.find_one = AsyncMock()
    collection.update_one = AsyncMock()
    collection.delete_one = AsyncMock()
    return collection


@pytest_asyncio.fixture
def mock_db(mock_collection):
    db = MagicMock()
    db.__getitem__.return_value = mock_collection
    return db


@pytest_asyncio.fixture
def account_repository(mock_db):
    return AccountRepository(db=mock_db)


@pytest.fixture
def sample_account_data():
    now = datetime.now()
    return {
        "name": "Test User",
        "iban": "ES1234567890123456789012",
        "cards": ["card1", "card2"],
        "creation_date": now,
        "email": "test@example.com",
        "subscription": "premium",
        "balance": 1000,
        "isBlocked": False,
        "isDeleted": False,
        "_id": "mock_object_id_123"
        }


async def test_insert_account(account_repository, mock_collection, sample_account_data):
    account_base = AccountBase(**sample_account_data)
    
    mock_insert_result = MagicMock()
    mock_insert_result.inserted_id = sample_account_data["_id"]
    mock_collection.insert_one.return_value = mock_insert_result
    mock_collection.find_one.return_value = sample_account_data
    
    result = await account_repository.insert_account(account_base)
    
    mock_collection.insert_one.assert_called_once_with(account_base.model_dump(by_alias=True))
    mock_collection.find_one.assert_called_once_with({"_id": mock_insert_result.inserted_id})
    assert isinstance(result, AccountView)
    assert result.iban == sample_account_data["iban"]


async def test_find_account_by_iban_found(account_repository, mock_collection, sample_account_data):
    iban = sample_account_data["iban"]
    mock_collection.find_one.return_value = sample_account_data
    
    result = await account_repository.find_account_by_iban(iban)
    
    mock_collection.find_one.assert_called_once_with({"iban": iban})
    assert isinstance(result, AccountView)
    assert result.iban == iban


async def test_find_account_by_iban_not_found(account_repository, mock_collection):
    iban = "ES_NON_EXISTENT"
    mock_collection.find_one.return_value = None
    
    result = await account_repository.find_account_by_iban(iban)
    
    mock_collection.find_one.assert_called_once_with({"iban": iban})
    assert result is None


async def test_delete_account_by_iban_success(account_repository, mock_collection):
    iban = "ES_TO_DELETE"
    
    mock_delete_result = MagicMock()
    mock_delete_result.deleted_count = 1
    mock_collection.delete_one.return_value = mock_delete_result
    
    result = await account_repository.delete_account_by_iban(iban)
    
    mock_collection.delete_one.assert_called_once_with({"iban": iban})
    
    assert result is True


async def test_delete_account_by_iban_failure(account_repository, mock_collection):
    iban = "ES_NON_EXISTENT"
    
    mock_delete_result = MagicMock()
    mock_delete_result.deleted_count = 0
    mock_collection.delete_one.return_value = mock_delete_result
    
    result = await account_repository.delete_account_by_iban(iban)
    
    mock_collection.delete_one.assert_called_once_with({"iban": iban})
    
    assert result is False


async def test_update_account_balance(account_repository, mock_collection, sample_account_data):
    iban = sample_account_data["iban"]
    new_balance = 5000
    update_data = AccountUpdatebalance(iban=iban, balance=new_balance)
    
    updated_doc = sample_account_data.copy()
    updated_doc["balance"] = new_balance
    
    mock_collection.find_one.return_value = updated_doc
    
    result = await account_repository.update_account_balance(iban, update_data)
    
    expected_update = {"$set": update_data.model_dump(exclude_unset=True)}
    mock_collection.update_one.assert_called_once_with({"iban": iban}, expected_update)
    assert result.balance == new_balance


async def test_update_account_no_email(account_repository, mock_collection, sample_account_data):
    iban = sample_account_data["iban"]
    update_data = AccountUpdate(name="New Name", subscription="basic")
    
    updated_doc = sample_account_data.copy()
    updated_doc["name"] = "New Name"
    updated_doc["subscription"] = "basic"
    
    mock_collection.find_one.return_value = updated_doc
    
    result = await account_repository.update_account(iban, update_data)
    
    expected_update = {"$set": {"name": "New Name", "subscription": "basic"}}
    mock_collection.update_one.assert_called_once_with({"iban": iban}, expected_update)
    assert result.name == "New Name"
    assert result.subscription == "basic"


async def test_update_account_no_data(account_repository, mock_collection, sample_account_data):
    iban = sample_account_data["iban"]
    update_data = AccountUpdate()
    
    mock_collection.find_one.return_value = sample_account_data
    
    # Act
    result = await account_repository.update_account(iban, update_data)
    
    # Assert
    mock_collection.update_one.assert_not_called()
    mock_collection.find_one.assert_called_once_with({"iban": iban})
    assert result.name == sample_account_data["name"]


async def test_block_account_by_iban(account_repository, mock_collection, sample_account_data):
    iban = sample_account_data["iban"]
    
    blocked_doc = sample_account_data.copy()
    blocked_doc["isBlocked"] = True
    
    mock_collection.find_one.return_value = blocked_doc
    
    result = await account_repository.block_account_by_iban(iban)
    
    mock_collection.update_one.assert_called_once_with(
        {"iban": iban},
        {"$set": {"isBlocked": True}}
        )
    mock_collection.find_one.assert_called_once_with({"iban": iban})
    assert result.isBlocked is True


async def test_unblock_account_by_iban(account_repository, mock_collection, sample_account_data):
    iban = sample_account_data["iban"]
    
    mock_collection.find_one.return_value = sample_account_data
    
    result = await account_repository.unblock_account_by_iban(iban)
    
    mock_collection.update_one.assert_called_once_with(
        {"iban": iban},
        {"$set": {"isBlocked": False}}
        )
    mock_collection.find_one.assert_called_once_with({"iban": iban})
    assert result.isBlocked is False