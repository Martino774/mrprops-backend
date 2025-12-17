from fastapi.testclient import TestClient
from main import app
from database import SessionLocal
from models import User
from routers.auth import verify_password

client = TestClient(app)

def run():
    email = 'mateo@mateo.mateo'
    payload = {
        'full_name': 'Mateo',
        'email': email,
        'phone': '+5491199999999',
        'password': 'mateooo'
    }

    print('Attempting register:', payload['email'])
    r = client.post('/api/auth/register', json=payload)
    print('Response status:', r.status_code)
    try:
        print('Response body:', r.json())
    except Exception as e:
        print('Response body not JSON:', e)

    db = SessionLocal()
    try:
        u = db.query(User).filter(User.email == email).first()
        if u:
            print('User found in DB:', u.id, u.email)
            print('Password hash:', u.password_hash)
            print('Password verifies?:', verify_password(payload['password'], u.password_hash))
        else:
            print('User NOT found in DB')
    finally:
        db.close()

if __name__ == '__main__':
    run()
