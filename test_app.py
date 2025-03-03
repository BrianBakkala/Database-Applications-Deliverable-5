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


def test_render_crud(client):
    table = "teams"
    response = client.get(f"/crud/{table}")
    assert response.status_code == 200
    assert b"teams" in response.data


def test_render_set_ops(client):
    set_op = "union"
    response = client.get(f"/set-ops/{set_op}")
    assert response.status_code == 200
    assert b"Union" in response.data
    assert b"Description" in response.data
    assert b"Query" in response.data


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
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection

        mock_connection.cursor.return_value = mock_cursor

        mock_run_query = MagicMock()

        db_helper = DBHelper("localhost", "user", "password", "test_db")
        db_helper.run_query = mock_run_query  # Replace the method with a mock

        # Test input
        table = "users"
        data = {"id": 1, "name": "John Doe", "email": "john@example.com"}

        # Call
        db_helper.create(table, data)

        expected_query = "INSERT INTO users (id, name, email) VALUES (%s, %s, %s);"

        mock_run_query.assert_called_once_with(expected_query, data)


def test_delete_success():
    mock_cursor = MagicMock()

    with patch("mysql.connector.connect") as mock_connect:
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection

        mock_connection.cursor.return_value = mock_cursor

        mock_run_query = MagicMock()
        mock_get_pk = MagicMock(return_value="id")

        db_helper = DBHelper("localhost", "user", "password", "test_db")
        db_helper.run_query = mock_run_query  # Replace the method with a mock
        db_helper.get_pk = mock_get_pk  # Mock the get_pk method

        # Test input
        table = "users"
        record_id = 1

        # Call
        db_helper.delete(table, record_id)

        expected_query = "DELETE FROM users WHERE id = 1;"

        mock_get_pk.assert_called_once_with(table)
        mock_run_query.assert_called_once_with(expected_query)


from unittest.mock import patch, MagicMock


def test_update_success():
    mock_cursor = MagicMock()

    with patch("mysql.connector.connect") as mock_connect:
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection

        mock_connection.cursor.return_value = mock_cursor

        mock_run_query = MagicMock()
        mock_get_pk = MagicMock(return_value="id")

        db_helper = DBHelper("localhost", "user", "password", "test_db")
        db_helper.run_query = mock_run_query  # Replace the method with a mock
        db_helper.get_pk = mock_get_pk  # Mock the get_pk method

        # Test input
        table = "users"
        record_id = 1
        data = {"name": "John Doe", "email": "john.doe@example.com"}

        # Call
        db_helper.update(table, record_id, data)

        expected_query = "UPDATE users SET name = %s, email = %s WHERE id = 1;"
        expected_params = ("John Doe", "john.doe@example.com")

        mock_get_pk.assert_called_once_with(table)
        mock_run_query.assert_called_once_with(expected_query, query_params=data)
