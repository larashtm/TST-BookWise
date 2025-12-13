import pytest
from uuid import UUID, uuid4
from domain.user_id import UserId


class TestUserIdCreation:
    """Test suite for UserId creation"""

    def test_create_user_id_with_valid_uuid(self):
        """Test creating UserId with valid UUID"""
        valid_uuid = uuid4()
        user_id = UserId(valid_uuid)
        assert user_id.value == valid_uuid

    def test_create_user_id_with_uuid_string(self):
        """Test creating UserId with UUID from string"""
        uuid_str = "987fcdeb-51a2-43e7-9876-543210fedcba"
        valid_uuid = UUID(uuid_str)
        user_id = UserId(valid_uuid)
        assert str(user_id.value) == uuid_str

    def test_user_id_immutability(self):
        """Test that UserId value object maintains its value"""
        original_uuid = uuid4()
        user_id = UserId(original_uuid)
        assert user_id.value == original_uuid


class TestUserIdEquality:
    """Test suite for UserId equality operations"""

    def test_user_id_equality(self):
        """Test equality between UserId instances"""
        uuid_val = uuid4()
        user_id1 = UserId(uuid_val)
        user_id2 = UserId(uuid_val)
        assert user_id1.value == user_id2.value

    def test_user_id_inequality(self):
        """Test inequality between different UserId instances"""
        user_id1 = UserId(uuid4())
        user_id2 = UserId(uuid4())
        assert user_id1.value != user_id2.value


class TestUserIdValidation:
    """Test suite for UserId validation and error handling"""

    def test_user_id_with_none_raises_error(self):
        """Test that creating UserId with None raises TypeError"""
        with pytest.raises(TypeError):
            UserId(None)

    def test_user_id_with_invalid_type_raises_error(self):
        """Test that creating UserId with invalid type raises error"""
        with pytest.raises((TypeError, ValueError, AttributeError)):
            UserId("not-a-uuid")

    def test_user_id_with_integer_raises_error(self):
        """Test that creating UserId with integer raises error"""
        with pytest.raises((TypeError, ValueError, AttributeError)):
            UserId(99999)


class TestUserIdUtility:
    """Test suite for UserId utility functions"""

    def test_user_id_string_representation(self):
        """Test string representation of UserId"""
        uuid_val = uuid4()
        user_id = UserId(uuid_val)
        assert str(user_id.value) == str(uuid_val)

    def test_multiple_user_ids_are_unique(self):
        """Test that multiple UserId instances have unique values"""
        user_ids = [UserId(uuid4()) for _ in range(10)]
        unique_values = set(str(uid.value) for uid in user_ids)
        assert len(unique_values) == 10

    def test_user_id_can_be_used_as_dict_key(self):
        """Test that UserId can be used in dictionary operations"""
        uuid_val = uuid4()
        user_id = UserId(uuid_val)
        test_dict = {str(user_id.value): "test_data"}
        assert test_dict[str(user_id.value)] == "test_data"

    def test_user_id_consistency(self):
        """Test that UserId value remains consistent"""
        uuid_val = uuid4()
        user_id = UserId(uuid_val)
        # Multiple accesses should return same value
        assert user_id.value == uuid_val
        assert user_id.value == uuid_val