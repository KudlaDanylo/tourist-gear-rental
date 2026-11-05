from date_helper import DateHelper

class SessionManager:
    def __init__(self):
        self.current_user = None
        self.saved_dates = None

    def set_current_user(self, user):
        self.current_user = user

    def set_rental_dates(self, start_str: str, end_str: str):
        dates, error = DateHelper.parse_rental_dates(start_str, end_str)
        if error:
            return error
        self.saved_dates = dates
        return None

    def get_rental_dates(self):
        return self.saved_dates

    def clear_dates(self):
        self.saved_dates = None

    def clear_session(self):
        self.current_user = None
        self.saved_dates = None

    def is_authenticated(self):
        return self.current_user is not None