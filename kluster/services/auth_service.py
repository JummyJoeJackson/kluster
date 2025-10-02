from typing import Optional
from kluster.models import db, User
import structlog

log = structlog.get_logger()

class AuthService:
    @staticmethod
    def register(email: str, username: str, password: str) -> User:
        if User.query.filter((User.email == email) | (User.username == username)).first():
            log.info("auth_register_conflict", email=email, username=username)
            raise ValueError("Email or username already exists")
        user = User(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        log.info("auth_register_success", user_id=user.id)
        return user

    @staticmethod
    def find_by_email(email: str) -> Optional[User]:
        return User.query.filter_by(email=email).first()
