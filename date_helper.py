from datetime import datetime

class DateHelper:
    @staticmethod
    def parse_rental_dates(start_str: str, end_str: str):
        start_date = datetime.strptime(start_str, "%Y.%m.%d").date()
        end_date = datetime.strptime(end_str, "%Y.%m.%d").date()
        if start_date >= end_date:
            return None, "Помилка: Час завершення має бути пізнішим за час початку!"
        return (start_date, end_date), None