import pytest
import requests
from app.srv import LIMIT


@pytest.mark.parametrize("input_text,expected", [
    ("hello world", "world hello"),
    ("a b c", "c b a"),
    ("testing reverse", "reverse testing"),
    ("one", "one"),
    ("", "")
])
def test_reverse_positive(flask_container, api_base_url, input_text, expected):
    """Test normal sentence reversal with various inputs"""
    response = requests.get(f"{api_base_url}/reverse?in={input_text}")
    assert response.status_code == 200
    assert response.json()['result'] == expected

def test_reverse_empty(flask_container, api_base_url):
    """Test empty input"""
    response = requests.get(f"{api_base_url}/reverse")
    assert response.status_code == 200
    assert response.json()['result'] == ''

def test_reverse_long(flask_container, api_base_url):
    """Test input longer than limit"""
    long_text = ' '.join(['word'] * LIMIT)
    response = requests.get(f"{api_base_url}/reverse?in={long_text}")
    assert response.status_code == 200
    assert len(response.json()['result']) <= LIMIT

def test_reverse_special_chars(flask_container, api_base_url):
    """Test with special characters"""
    response = requests.get(f"{api_base_url}/reverse?in=hello! world?")
    assert response.status_code == 200
    assert response.json()['result'] == 'world? hello!'

@pytest.mark.run(order=1)
def test_restore_initial(flask_container, api_base_url):
    """Test initial restore state"""
    response = requests.get(f"{api_base_url}/restore")
    assert response.status_code == 200
    assert response.json()['result'] == ''

def test_reverse_then_restore(flask_container, api_base_url):
    """Test DB persistence between operations"""
    requests.get(f"{api_base_url}/reverse?in=hello world")
    response = requests.get(f"{api_base_url}/restore")
    assert response.status_code == 200
    assert response.json()['result'] == 'world hello'
    requests.get(f"{api_base_url}/reverse?in=bye world")
    response = requests.get(f"{api_base_url}/restore")
    assert response.status_code == 200
    assert response.json()['result'] == 'world bye'
