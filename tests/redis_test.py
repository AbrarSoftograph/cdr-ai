"""Redis Connection Tests

Industry-standard test cases for Redis connectivity using pytest.
Tests connection, authentication, read/write operations, and error handling.
"""

import os
import sys
import pytest
from dotenv import load_dotenv

# Load environment variables once at module level
load_dotenv()


class TestRedisConnection:
    """Industry-standard Redis connection test suite."""

    @pytest.fixture
    def redis_config(self):
        """Fixture providing Redis configuration from environment variables."""
        return {
            "host": os.getenv("REDIS_HOST", "localhost"),
            "port": int(os.getenv("REDIS_PORT", "6379")),
            "username": os.getenv("REDIS_USERNAME", ""),
            "password": os.getenv("REDIS_PASSWORD", ""),
            "db": int(os.getenv("REDIS_DB", "0")),
        }

    @pytest.fixture
    def redis_client(self, redis_config):
        """Fixture providing Redis client connection."""
        try:
            import redis
        except ImportError:
            pytest.skip("redis library not installed. Install with: pip install redis")

        config = redis_config
        if config["username"] and config["password"]:
            client = redis.Redis(
                host=config["host"],
                port=config["port"],
                db=config["db"],
                username=config["username"],
                password=config["password"],
            )
        else:
            client = redis.Redis(host=config["host"], port=config["port"], db=config["db"])
        return client

    def test_redis_connection(self, redis_client):
        """Test that Redis server is accessible and responds to ping."""
        # Act & Assert
        assert redis_client.ping() is True

    def test_redis_basic_write_read(self, redis_client):
        """Test basic write and read operations."""
        # Arrange
        test_key = "test_integration_key"
        test_value = "integration_test_value"

        try:
            # Act
            redis_client.set(test_key, test_value)
            retrieved_value = redis_client.get(test_key)

            # Assert
            assert retrieved_value is not None
            assert retrieved_value.decode("utf-8") == test_value

        finally:
            # Cleanup
            redis_client.delete(test_key)

    def test_redis_key_expiration(self, redis_client):
        """Test Redis key expiration functionality."""
        # Arrange
        test_key = "test_expiration_key"
        test_value = "expires_quickly"
        ttl_seconds = 2

        try:
            # Act
            redis_client.setex(test_key, ttl_seconds, test_value)

            # Assert - Key should exist initially
            assert redis_client.exists(test_key) == 1

            # Wait for expiration
            import time

            time.sleep(ttl_seconds + 1)

            # Assert - Key should be gone
            assert redis_client.exists(test_key) == 0

        finally:
            # Cleanup (in case expiration didn't work)
            redis_client.delete(test_key)

    def test_redis_authentication_configured(self, redis_config):
        """Test that authentication is properly configured when credentials exist."""
        config = redis_config

        if config["username"] and config["password"]:
            # If credentials are provided, authentication should work
            try:
                import redis

                client = redis.Redis(
                    host=config["host"],
                    port=config["port"],
                    db=config["db"],
                    username=config["username"],
                    password=config["password"],
                )
                assert client.ping() is True
            except redis.AuthenticationError:
                pytest.fail("Authentication failed despite credentials being configured")
        else:
            # If no credentials, should still connect
            try:
                import redis

                client = redis.Redis(host=config["host"], port=config["port"], db=config["db"])
                assert client.ping() is True
            except redis.AuthenticationError:
                pytest.fail("Authentication error when no credentials expected")


def run_standalone_tests():
    """Run tests in standalone mode with human-readable output."""
    print("Redis Connection Test")
    print("=" * 40)

    try:
        import redis
    except ImportError:
        print("ERROR: Redis library not installed. Install with: pip install redis")
        return False

    # Get configuration
    config = {
        "host": os.getenv("REDIS_HOST", "localhost"),
        "port": int(os.getenv("REDIS_PORT", "6379")),
        "username": os.getenv("REDIS_USERNAME", ""),
        "password": os.getenv("REDIS_PASSWORD", ""),
        "db": int(os.getenv("REDIS_DB", "0")),
    }

    print(f"Host: {config['host']}")
    print(f"Port: {config['port']}")
    print(f"Database: {config['db']}")
    print()

    try:
        # Create client
        if config["username"] and config["password"]:
            r = redis.Redis(
                host=config["host"],
                port=config["port"],
                db=config["db"],
                username=config["username"],
                password=config["password"],
            )
        else:
            r = redis.Redis(host=config["host"], port=config["port"], db=config["db"])

        # Test 1: Connection
        print("PASS: Testing connection...")
        r.ping()

        # Test 2: Write/Read
        print("PASS: Testing read/write...")
        test_key = "standalone_test_key"
        test_value = "standalone_test_value"
        r.set(test_key, test_value)
        value = r.get(test_key)
        assert value.decode() == test_value
        r.delete(test_key)

        # Test 3: Cleanup
        print("PASS: Tests completed successfully")

        print("\nSUCCESS: All Redis tests passed!")
        print("Redis connection is working correctly.")
        return True

    except redis.ConnectionError:
        print("ERROR: Cannot connect to Redis server")
        print("- Make sure Redis is running: docker run -d --name redis -p 6379:6379 redis")
        return False
    except redis.AuthenticationError:
        print("ERROR: Redis authentication failed")
        print("- Check REDIS_USERNAME and REDIS_PASSWORD in .env file")
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        return False


if __name__ == "__main__":
    # Run standalone tests when executed directly
    success = run_standalone_tests()
    sys.exit(0 if success else 1)
