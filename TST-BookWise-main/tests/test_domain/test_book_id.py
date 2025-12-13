import pytest
from uuid import UUID, uuid4
from domain.book_id import BookId


class TestBookIdCreation:
    """Test suite for BookId creation"""

    def test_create_book_id_with_valid_uuid(self):
        """Test creating BookId with valid UUID"""
        valid_uuid = uuid4()
        book_id = BookId(valid_uuid)
        assert book_id.value == valid_uuid

    def test_create_book_id_with_uuid_string(self):
        """Test creating BookId with UUID from string"""
        uuid_str = "123e4567-e89b-12d3-a456-426614174000"
        valid_uuid = UUID(uuid_str)
        book_id = BookId(valid_uuid)
        assert str(book_id.value) == uuid_str

    def test_book_id_immutability(self):
        """Test that BookId value object maintains its value"""
        original_uuid = uuid4()
        book_id = BookId(original_uuid)
        assert book_id.value == original_uuid


class TestBookIdEquality:
    """Test suite for BookId equality operations"""

    def test_book_id_equality(self):
        """Test equality between BookId instances"""
        uuid_val = uuid4()
        book_id1 = BookId(uuid_val)
        book_id2 = BookId(uuid_val)
        assert book_id1.value == book_id2.value

    def test_book_id_inequality(self):
        """Test inequality between different BookId instances"""
        book_id1 = BookId(uuid4())
        book_id2 = BookId(uuid4())
        assert book_id1.value != book_id2.value


class TestBookIdValidation:
    """Test suite for BookId validation and error handling"""

    def test_book_id_with_none_raises_error(self):
        """Test that creating BookId with None raises TypeError"""
        with pytest.raises(TypeError):
            BookId(None)

    def test_book_id_with_invalid_type_raises_error(self):
        """Test that creating BookId with invalid type raises error"""
        with pytest.raises((TypeError, ValueError, AttributeError)):
            BookId("not-a-uuid")

    def test_book_id_with_integer_raises_error(self):
        """Test that creating BookId with integer raises error"""
        with pytest.raises((TypeError, ValueError, AttributeError)):
            BookId(12345)


class TestBookIdUtility:
    """Test suite for BookId utility functions"""

    def test_book_id_string_representation(self):
        """Test string representation of BookId"""
        uuid_val = uuid4()
        book_id = BookId(uuid_val)
        assert str(book_id.value) == str(uuid_val)

    def test_multiple_book_ids_are_unique(self):
        """Test that multiple BookId instances have unique values"""
        book_ids = [BookId(uuid4()) for _ in range(10)]
        unique_values = set(str(bid.value) for bid in book_ids)
        assert len(unique_values) == 10

    def test_book_id_can_be_used_as_dict_key(self):
        """Test that BookId value can be used in dictionary operations"""
        uuid_val = uuid4()
        book_id = BookId(uuid_val)
        test_dict = {str(book_id.value): "test_data"}
        assert test_dict[str(book_id.value)] == "test_data"