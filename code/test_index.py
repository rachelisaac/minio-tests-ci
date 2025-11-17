import io
import string
import pytest
from unittest.mock import MagicMock, patch
from index import random_name, random_data, client, bucket_name

def test_random_name_length():
    name = random_name(10)
    assert len(name) == 10
    for c in name:
        assert c in string.ascii_lowercase + string.digits

def test_random_data_length_and_type():
    data1 = random_data(50)
    data2 = random_data(50)
    assert isinstance(data1, bytes)
    assert isinstance(data2, bytes)
    assert len(data1) == 50
    assert len(data2) == 50
    assert data1 != data2

@patch("index.client")
def test_bucket_exists_true(mock_client):
    mock_client.bucket_exists.return_value = True
    exists = mock_client.bucket_exists(bucket_name)
    mock_client.bucket_exists.assert_called_with(bucket_name)
    assert exists is True

@patch("index.client")
def test_bucket_exists_false(mock_client):
    mock_client.bucket_exists.return_value = False
    exists = mock_client.bucket_exists(bucket_name)
    mock_client.bucket_exists.assert_called_with(bucket_name)
    assert exists is False

@patch("index.client")
def test_make_bucket(mock_client):
    mock_client.make_bucket.return_value = None
    result = mock_client.make_bucket(bucket_name)
    assert result is None
    mock_client.make_bucket.assert_called_with(bucket_name)

@patch("index.client")
def test_put_object(mock_client):
    mock_client.put_object.return_value = None
    data = io.BytesIO(b"test")
    content = data.getvalue()
    mock_client.put_object(
        bucket_name,
        "file.txt",
        data,
        length=len(content),
        content_type="text/plain"
    )
    mock_client.put_object.assert_called_once_with(
        bucket_name,
        "file.txt",
        data,
        length=len(content),
        content_type="text/plain"
    )


@patch("index.client")
def test_list_objects(mock_client):
    # Arrange
    mock_obj = MagicMock()
    mock_obj.object_name = "file.txt"
    mock_obj.size = 50
    mock_client.list_objects.return_value = [mock_obj]
    # Act
    objects = mock_client.list_objects(bucket_name, recursive=True)
    objects = list(objects)
    # Assert
    mock_client.list_objects.assert_called_once_with(bucket_name, recursive=True)
    assert len(objects) == 1
    assert objects[0].object_name == "file.txt"
    assert objects[0].size == 50

@patch("index.client")
def test_get_object(mock_client):
    mock_response = MagicMock()
    mock_response.read.return_value = b"hello world"
    mock_response.close.return_value = None
    mock_response.release_conn.return_value = None
    mock_client.get_object.return_value = mock_response

    response = mock_client.get_object(bucket_name, "file.txt")
    data = response.read().decode("utf-8")
    response.close()
    response.release_conn()

    mock_client.get_object.assert_called_with(bucket_name, "file.txt")
    assert data == "hello world"

@patch("index.client")
def test_remove_object(mock_client):
    mock_client.remove_object.return_value = None
    mock_client.remove_object(bucket_name, "file.txt")
    mock_client.remove_object.assert_called_with(bucket_name, "file.txt")
