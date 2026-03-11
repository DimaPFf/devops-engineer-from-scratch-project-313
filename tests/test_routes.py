import pytest
from unittest.mock import Mock
from flask import json as flask_json

from src.main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_ping(client):
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.data == b'pong'

def test_get_links_success(client, mocker):
    mock_get_all = mocker.patch('src.main.get_all_links')
    
    mock_link = Mock()
    mock_link.model_dump.return_value = {
        "created_at": "2026-02-21T18:02:55.083611",
        "id": 1,
        "original_url": "https://chat.qwen.ai",
        "short_name": "five",
        "short_url": "https://short.com/five",
    }
    mock_get_all.return_value = [mock_link]
    
    response = client.get('/api/links')
    
    assert response.status_code == 200
    data = flask_json.loads(response.data)
    assert len(data) == 1
    assert data[0]['id'] == 1
    mock_get_all.assert_called_once()

def test_get_links_with_pagination_not_valid_range_1(client, mocker):
    mock_get_links_with_pagination = mocker.patch('src.main.get_links_with_pagination')
    
    mock_get_links_with_pagination.return_value = []
    
    response = client.get('/api/links?range=[2,1]')
    
    assert response.status_code == 200
    data = flask_json.loads(response.data)
    assert len(data) == 0
    mock_get_links_with_pagination.assert_called_once()

def test_get_links_with_pagination_not_valid_range_2(client, mocker):
    mock_get_links_with_pagination = mocker.patch('src.main.get_links_with_pagination')
    
    mock_get_links_with_pagination.return_value = []
    
    response = client.get('/api/links?range=[-1,1]')
    
    assert response.status_code == 200
    data = flask_json.loads(response.data)
    assert len(data) == 0
    mock_get_links_with_pagination.assert_called_once()

def test_get_links_with_pagination_success(client, mocker):
    mock_get_links_with_pagination = mocker.patch('src.main.get_links_with_pagination')

    mock_link = Mock()
    mock_link.model_dump.return_value = {
        "created_at": "2026-02-21T18:02:55.083611",
        "id": 1,
        "original_url": "https://chat.qwen.ai",
        "short_name": "five",
        "short_url": "https://short.com/five",
    }
    
    mock_get_links_with_pagination.return_value = [mock_link, mock_link]
    
    response = client.get('/api/links?range=[1,2]')
    
    assert response.status_code == 200
    data = flask_json.loads(response.data)
    assert len(data) == 2
    assert data[0]['id'] == 1
    mock_get_links_with_pagination.assert_called_once()

def test_post_links_success(client, mocker):
    mock_create = mocker.patch('src.main.create_link')
    mocker.patch('src.main.validate_data', return_value=None)
    
    mock_link = Mock()
    mock_link.model_dump.return_value = {
        'id': 1,
        'original_url': 'https://example.com',
        'short_name': 'ex',
        "short_url": "https://short.com/ex",
        "created_at": "2026-02-21T18:02:55.083611",
    }
    mock_create.return_value = mock_link
    
    response = client.post(
        '/api/links',
        data=flask_json.dumps({
            'original_url': 'https://example.com',
            'short_name': 'ex'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = flask_json.loads(response.data)
    assert data['id'] == 1
    mock_create.assert_called_once_with(
        original_url='https://example.com',
        short_name='ex'
    )


def test_get_link_not_found(client, mocker):
    mocker.patch('src.main.get_link_by_id', return_value=None)
    
    response = client.get('/api/links/999')
    
    assert response.status_code == 404
    data = flask_json.loads(response.data)
    assert data['error'] == 'Not found'


def test_delete_link_route(client, mocker):
    mocker.patch('src.main.delete_link', return_value=True)
    
    response = client.delete('/api/links/42')
    
    assert response.status_code == 204
    assert response.data == b''


def test_put_link_not_found(client, mocker):
    mocker.patch('src.main.validate_data', return_value=None)
    mocker.patch('src.main.update_link', return_value=None)
    
    response = client.put(
        '/api/links/999',
        data=flask_json.dumps({
            'original_url': 'https://updated.com',
            'short_name': 'up'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 404
    data = flask_json.loads(response.data)
    assert data['error'] == 'Not found'