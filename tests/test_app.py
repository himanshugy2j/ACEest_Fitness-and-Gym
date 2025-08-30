import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_health(client):
    rv = client.get('/health')
    assert rv.status_code == 200
    assert rv.get_json()['status'] == 'ok'

def test_signup_and_login(client):
    # Signup
    rv = client.post('/signup', data={'username': 'testuser', 'password': 'testpass'}, follow_redirects=True)
    assert rv.status_code == 200
    assert b'login' in rv.data or b'dashboard' in rv.dat

    # Login
    rv = client.post('/login', data={'username': 'testuser', 'password': 'testpass'}, follow_redirects=True)
    assert b'Logged in successfully' in rv.data
    assert b'Dashboard' in rv.data

def test_dashboard_requires_login(client):
    rv = client.get('/dashboard')
    # Should redirect to login
    assert rv.status_code == 302
    assert '/login' in rv.headers['Location']

def test_add_strength_workout(client):
    # Signup and login
    client.post('/signup', data={'username': 'strengthuser', 'password': 'pass'}, follow_redirects=True)
    client.post('/login', data={'username': 'strengthuser', 'password': 'pass'}, follow_redirects=True)

    # Add strength workout
    rv = client.post('/dashboard', data={
        'form_type': 'strength',
        'exercise': 'Bench Press',
        'reps': '10',
        'weight': '80'
    }, follow_redirects=True)
    assert b'Strength workout added' in rv.data
    assert b'Bench Press' in rv.data

def test_add_cardio_workout(client):
    # Signup and login
    client.post('/signup', data={'username': 'cardiouser', 'password': 'pass'}, follow_redirects=True)
    client.post('/login', data={'username': 'cardiouser', 'password': 'pass'}, follow_redirects=True)

    # Add cardio workout
    rv = client.post('/dashboard', data={
        'form_type': 'cardio',
        'activity': 'Running',
        'duration': '30',
        'distance': '5',
        'calories': '300'
    }, follow_redirects=True)
    assert b'Cardio workout added' in rv.data
    assert b'Running' in rv.data