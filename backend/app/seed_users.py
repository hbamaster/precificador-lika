from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Usuario
from app.auth import get_password_hash

def seed():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    users = [
        {"username": "likamagazine", "password": "Lik@M@g@2024"},
        {"username": "tester", "password": "tester"}
    ]

    for user in users:
        existing = db.query(Usuario).filter(Usuario.username == user["username"]).first()
        if not existing:
            hashed = get_password_hash(user["password"])
            new_user = Usuario(username=user["username"], hashed_password=hashed)
            db.add(new_user)
            print(f"Usuário criado: {user['username']}")
        else:
            print(f"Usuário já existe: {user['username']}")

    db.commit()
    db.close()

if __name__ == "__main__":
    seed()