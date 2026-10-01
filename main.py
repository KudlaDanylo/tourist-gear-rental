from db import Bd
from auth_service import AuthService, SessionManager
from ui import ConsoleUI


def main():
    db = Bd()
    db_session = db.get_session()

    session_manager = SessionManager()
    auth_service = AuthService(db_session, session_manager)

    app_ui = ConsoleUI(auth_service, session_manager)
    app_ui.run()
if __name__ == "__main__":
    main()