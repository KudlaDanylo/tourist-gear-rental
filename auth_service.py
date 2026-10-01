import bcrypt
from table import Client


class SessionManager:
    def __init__(self):
        self.current_user = None

    def set_current_user(self, user):
        self.current_user = user

    def clear_session(self):
        self.current_user = None

    def is_authenticated(self):
        return self.current_user is not None


class AuthService:
    def __init__(self, db_session, session_manager: SessionManager):
        self.db_session = db_session
        self.session_manager = session_manager

    def _hash_password(self, password: str):
        password_to_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hash_bytes = bcrypt.hashpw(password_to_bytes, salt)
        return hash_bytes.decode("utf-8")

    def _verify_password(self, hashed_password: str, provided_password: str):
        return bcrypt.checkpw(provided_password.encode("utf-8"), hashed_password.encode("utf-8"))

    def register(self, name: str , age: str , number: str, email: str , password: str):
        audit_email = self.db_session.query(Client).filter_by(email=email).first()
        if audit_email:
            raise ValueError("Користувач з такою електронною поштою вже існує")

        audit_number = self.db_session.query(Client).filter_by(number=number).first()
        if audit_number:
            raise ValueError("Цей номер телефону все зареєстрований")

        hash_password = self._hash_password(password)
        is_user_admin = (email == "admin@mail.com")
        new_client = Client(
            name=name,
            age=age,
            number=number,
            email=email,
            password_hash=hash_password,
            is_admin=is_user_admin
        )
        self.db_session.add(new_client)
        self.db_session.commit()
        return new_client
        
    def login(self, email: str, password: str):
        client = self.db_session.query(Client).filter_by(email=email).first()
        if not client or not self._verify_password(client.password_hash, password):
            raise ValueError("Невірна пошта або пароль")
        self.session_manager.set_current_user(client)
        return True

    def logout(self):
        self.session_manager.clear_session()