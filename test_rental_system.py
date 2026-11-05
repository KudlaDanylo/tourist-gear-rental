import unittest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base
from client import Client
from equipment import Equipment
from rental import Rental
from auth_service import AuthService
from rental_service import RentalService
from session_manager import SessionManager
from date_helper import DateHelper

class TestDateHelper(unittest.TestCase):
    def test_parse_dates_success(self):
        dates, error = DateHelper.parse_rental_dates("2026.10.20","2026.10.22")
        self.assertIsNone(error)
        self.assertEqual(dates[0], date(2026, 10, 20))
        self.assertEqual(dates[1], date(2026, 10, 22))

    def test_parse_dates_invalid_format(self):
        dates, error = DateHelper.parse_rental_dates("20.10.2026", "2026.10.22")
        self.assertIsNone(dates)
        self.assertIn("Неправильний формат", error)

    def test_parse_dates_wrong_logic(self):
        dates, error = DateHelper.parse_rental_dates("2026.10.22","2026.10.20")
        self.assertIsNone(dates)
        self.assertIsNotNone(error)

class BaseDBTest(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.db_session = Session()

    def tearDown(self):
        self.db_session.close()
        Base.metadata.drop_all(self.engine)

class TestAuthService(BaseDBTest):
    def test_register_success(self):
        session_mgr = SessionManager()
        auth = AuthService(self.db_session, session_mgr)
        errors = auth.register("Іван", "20", "0991112233", "ivan@mail.com", "qwerty")


        user = self.db_session.query(Client).filter_by(email="ivan@mail.com").first()
        self.assertIsNotNone(user)
        self.assertEqual(user.name, "Іван")

    def test_login_invalid_password(self):
        session_mgr = SessionManager()
        auth = AuthService(self.db_session, session_mgr)
        auth.register("Іван", "20", "0991112233", "ivan@mail.com", "qwerty")

        with self.assertRaises(ValueError) as context:
            auth.login("ivan@mail.com", "wrong_password")

        self.assertIn("Невірна пошта або пароль",str(context.exception))

    def test_login_success(self):
        session_mgr = SessionManager()
        auth = AuthService(self.db_session, session_mgr)
        auth.register("Іван", "20", "0991112233", "ivan@mail.com", "qwerty")
        user = auth.login("ivan@mail.com", "qwerty")
        self.assertTrue(user)

    def test_delete_user(self):
        session_mgr = SessionManager()
        auth = AuthService(self.db_session, session_mgr)
        auth.register("Олег", "30", "0501234567", "oleg@mail.com", "123123")
        user = self.db_session.query(Client).filter_by(email="oleg@mail.com").first()

        result = auth.delete_user(user.id)
        self.assertTrue(result)
        deleted_user = self.db_session.query(Client).filter_by(id=user.id).first()
        self.assertIsNone(deleted_user)

class TestRentalService(BaseDBTest):
    def test_is_item_available_logic(self):
        rental_service = RentalService(self.db_session)

        for i in range(15):
            item = Equipment(name=f"Спальник {i}", category="Сон", price=100, quantity=1)
            self.db_session.add(item)
        self.db_session.commit()

        start_d = date(2026, 10, 16)
        end_d = date(2026, 10, 20)
        items, has_more = rental_service.get_available_equipment_page(start_d, end_d, page=0, per_page=10)
        self.assertEqual(len(items), 10)
        self.assertTrue(has_more)

    def test_availability_on_different_dates(self):
        rental_service = RentalService(self.db_session)
        tent = Equipment(name="Намет", category="Кемпінг", price=250, quantity=1)
        self.db_session.add(tent)
        self.db_session.commit()
        rental_service.rent_equipment(1, tent.id, date(2026, 10, 10), date(2026, 10, 15))
        self.assertTrue(rental_service.is_item_available(tent.id, date(2026, 10, 15), date(2026, 10, 20)))

if __name__ == '__main__':
    unittest.main()