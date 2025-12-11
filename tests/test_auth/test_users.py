import pytest
from uuid import uuid4
from auth.users import (
    User, 
    hash_password, 
    verify_password, 
    get_user_by_username, 
    get_user_by_id, 
    USERS_DB
)


class TestUserClass:
    """Test suite for User class"""

    def test_user_creation(self):
        """Test creating a User instance"""
        user_id = uuid4()
        user = User(user_id, "testuser", "hashed_pwd", "peminjam")
        
        assert user.user_id == user_id
        assert user.username == "testuser"
        assert user.hashed_password == "hashed_pwd"
        assert user.role == "peminjam"
        assert user.disabled is False

    def test_user_with_disabled_flag(self):
        """Test creating a disabled user"""
        user_id = uuid4()
        user = User(user_id, "disabled_user", "hashed_pwd", "pengguna", disabled=True)
        
        assert user.disabled is True

    def test_user_attributes_accessible(self):
        """Test that all user attributes are accessible"""
        user_id = uuid4()
        user = User(user_id, "testuser", "hashed_pwd", "peminjam")
        
        assert hasattr(user, 'user_id')
        assert hasattr(user, 'username')
        assert hasattr(user, 'hashed_password')
        assert hasattr(user, 'role')
        assert hasattr(user, 'disabled')

    def test_user_peminjam_role(self):
        """Test creating user with peminjam role"""
        user = User(uuid4(), "peminjam_user", "pwd", "peminjam")
        assert user.role == "peminjam"

    def test_user_pengguna_role(self):
        """Test creating user with pengguna role"""
        user = User(uuid4(), "pengguna_user", "pwd", "pengguna")
        assert user.role == "pengguna"


class TestPasswordHashing:
    """Test suite for password hashing"""

    def test_hash_password_returns_string(self):
        """Test that hash_password returns a string"""
        hashed = hash_password("test123")
        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_hash_password_different_outputs(self):
        """Test that hashing same password twice gives different results (salt)"""
        hashed1 = hash_password("test123")
        hashed2 = hash_password("test123")
        # bcrypt adds salt, so hashes should be different
        assert hashed1 != hashed2

    def test_hash_password_not_plaintext(self):
        """Test that hashed password is not the same as plaintext"""
        password = "mypassword"
        hashed = hash_password(password)
        assert hashed != password

    def test_hash_password_with_long_password(self):
        """Test hashing password longer than 72 chars (bcrypt limit)"""
        long_password = "a" * 100
        hashed = hash_password(long_password)
        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_hash_password_with_special_characters(self):
        """Test hashing password with special characters"""
        password = "P@ssw0rd!#$%"
        hashed = hash_password(password)
        assert isinstance(hashed, str)

    def test_hash_password_empty_string(self):
        """Test hashing empty string"""
        hashed = hash_password("")
        assert isinstance(hashed, str)


class TestPasswordVerification:
    """Test suite for password verification"""

    def test_verify_correct_password(self):
        """Test verifying correct password"""
        password = "test123"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True

    def test_verify_incorrect_password(self):
        """Test verifying incorrect password"""
        password = "test123"
        wrong_password = "wrong123"
        hashed = hash_password(password)
        
        assert verify_password(wrong_password, hashed) is False

    def test_verify_case_sensitive(self):
        """Test that password verification is case sensitive"""
        password = "Test123"
        hashed = hash_password(password)
        
        assert verify_password("test123", hashed) is False

    def test_verify_with_special_characters(self):
        """Test verifying password with special characters"""
        password = "P@ssw0rd!#$"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True

    def test_verify_empty_password(self):
        """Test verifying empty password"""
        password = ""
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True

    def test_verify_long_password(self):
        """Test verifying password longer than 72 chars"""
        password = "a" * 100
        hashed = hash_password(password)
        
        # Due to 72 char limit, should still verify correctly
        assert verify_password(password, hashed) is True

    def test_verify_wrong_hash(self):
        """Test verifying password with wrong hash"""
        password = "test123"
        wrong_hash = hash_password("different_password")
        
        assert verify_password(password, wrong_hash) is False


class TestUserDatabase:
    """Test suite for user database operations"""

    def test_get_user_by_username_existing(self):
        """Test getting existing user by username"""
        user = get_user_by_username("pengguna1")
        
        assert user is not None
        assert user.username == "pengguna1"
        assert user.role == "pengguna"

    def test_get_user_by_username_non_existing(self):
        """Test getting non-existing user by username"""
        user = get_user_by_username("nonexistent")
        
        assert user is None

    def test_get_user_by_username_case_sensitive(self):
        """Test that username lookup is case sensitive"""
        user = get_user_by_username("PENGGUNA1")
        
        assert user is None

    def test_get_user_by_id_existing(self):
        """Test getting existing user by ID"""
        # Get a known user first
        known_user = get_user_by_username("peminjam1")
        
        # Now find by ID
        user = get_user_by_id(str(known_user.user_id))
        
        assert user is not None
        assert user.username == "peminjam1"
        assert user.user_id == known_user.user_id

    def test_get_user_by_id_non_existing(self):
        """Test getting non-existing user by ID"""
        fake_id = str(uuid4())
        user = get_user_by_id(fake_id)
        
        assert user is None

    def test_users_db_contains_default_users(self):
        """Test that USERS_DB contains default users"""
        assert "pengguna1" in USERS_DB
        assert "peminjam1" in USERS_DB

    def test_default_user_pengguna_credentials(self):
        """Test default pengguna user has correct credentials"""
        user = get_user_by_username("pengguna1")
        
        assert user is not None
        assert user.role == "pengguna"
        assert verify_password("pengguna123", user.hashed_password)

    def test_default_user_peminjam_credentials(self):
        """Test default peminjam user has correct credentials"""
        user = get_user_by_username("peminjam1")
        
        assert user is not None
        assert user.role == "peminjam"
        assert verify_password("pinjam123", user.hashed_password)

    def test_users_db_is_dict(self):
        """Test that USERS_DB is a dictionary"""
        assert isinstance(USERS_DB, dict)

    def test_users_in_db_are_user_objects(self):
        """Test that all values in USERS_DB are User objects"""
        for user in USERS_DB.values():
            assert isinstance(user, User)

    def test_get_user_by_id_with_uuid_object(self):
        """Test getting user by UUID object (not string)"""
        known_user = get_user_by_username("pengguna1")
        
        # Should handle UUID object conversion
        user = get_user_by_id(known_user.user_id)
        
        assert user is not None
        assert user.username == "pengguna1"


class TestUserIntegration:
    """Integration tests for user authentication"""

    def test_complete_auth_flow_success(self):
        """Test complete authentication flow with correct credentials"""
        username = "peminjam1"
        password = "pinjam123"
        
        # Get user
        user = get_user_by_username(username)
        assert user is not None
        
        # Verify password
        assert verify_password(password, user.hashed_password)
        
        # Check user properties
        assert user.role == "peminjam"
        assert user.disabled is False

    def test_complete_auth_flow_wrong_password(self):
        """Test authentication flow with wrong password"""
        username = "peminjam1"
        wrong_password = "wrongpass"
        
        user = get_user_by_username(username)
        assert user is not None
        
        assert verify_password(wrong_password, user.hashed_password) is False

    def test_complete_auth_flow_wrong_username(self):
        """Test authentication flow with wrong username"""
        username = "nonexistent"
        password = "anypass"
        
        user = get_user_by_username(username)
        assert user is None

    def test_both_default_users_exist(self):
        """Test that both default users exist and are valid"""
        peminjam = get_user_by_username("peminjam1")
        pengguna = get_user_by_username("pengguna1")
        
        assert peminjam is not None
        assert pengguna is not None
        assert peminjam.role == "peminjam"
        assert pengguna.role == "pengguna"