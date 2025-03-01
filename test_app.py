import pytest
from app import app, DBHelper
from unittest.mock import patch, MagicMock
from mysql.connector import Error


# fixture to create a test client for Flask app
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


# # # # # # #
# ROUTES
# # # # # # #
def test_homepage(client):
    response = client.get("/home/")
    assert response.status_code == 200
    assert b"Welcome" in response.data


# # # # # # #
# DB
# # # # # # #
def test_dbhelper_init_success():
    with patch("mysql.connector.connect") as mock_connect:
        mock_connect.return_value.is_connected.return_value = True
        db_helper = DBHelper("localhost", "user", "password", "test_db")
        assert db_helper.connection.is_connected() is True
        mock_connect.assert_called_once_with(
            host="localhost", user="user", password="password", database="test_db"
        )


def test_dbhelper_init_failure():
    with patch("mysql.connector.connect") as mock_connect:
        mock_connect.side_effect = Error("Connection failed")
        db_helper = DBHelper("localhost", "user", "password", "test_db")
        assert db_helper.connection is None


#  read method with a mocked connection
def test_read_success():

    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [{"id": 1, "name": "John"}]

    with patch("mysql.connector.connect") as mock_connect:
        # connection
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection

        # cursor
        mock_connection.cursor.return_value = mock_cursor

        db_helper = DBHelper("localhost", "user", "password", "test_db")

        result = db_helper.read("users")

        # Assert the results returned are as expected
        assert result == [{"id": 1, "name": "John"}]
        mock_cursor.execute.assert_called_once_with("SELECT * FROM users;")
        mock_cursor.fetchall.assert_called_once()


#  create method with a mocked connection
def test_create_success():
    mock_cursor = MagicMock()

    with patch("mysql.connector.connect") as mock_connect:
        # Mock the connection
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection

        # Mock the cursor
        mock_connection.cursor.return_value = mock_cursor

        # Mock run_query method
        mock_run_query = MagicMock()

        db_helper = DBHelper("localhost", "user", "password", "test_db")
        db_helper.run_query = mock_run_query  # Replace the method with a mock

        # Test input
        table = "users"
        data = {"id": 1, "name": "John Doe", "email": "john@example.com"}

        # Call the method
        db_helper.create(table, data)

        # Expected SQL Query
        expected_query = "INSERT INTO users (id, name, email) VALUES (%s, %s, %s);"

        # Assert `run_query` was called with the expected query and data
        mock_run_query.assert_called_once_with(expected_query, data)
