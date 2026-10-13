from db import Bd
from auth_service import AuthService, SessionManager
from equipment_service import EquipmentService
from ui import ConsoleUI


def main():
    db = Bd()
    db_session = db.get_session()

    session_manager = SessionManager()
    auth_service = AuthService(db_session, session_manager)
    equipment_service = EquipmentService(db_session)

    app_ui = ConsoleUI(auth_service, session_manager, equipment_service)
    app_ui.run()
main()