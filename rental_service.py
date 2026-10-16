from equipment import Equipment
from rental import Rental

class RentalService:
    def __init__(self,db_session):
        self.db_session = db_session

    def rent_equipment(self, client_id, equipment_id, start_time, end_time):
        item = self.db_session.query(Equipment).filter_by(id=equipment_id).first()

        overlapping_rentals = self.db_session.query(Rental).filter(
            Rental.equipment_id == equipment_id,
            Rental.start_time < end_time,
            Rental.end_time > start_time
        )
        events = []
        for i in overlapping_rentals:
            actual_start = max(i.start_time, start_time)
            actual_end = min(i.end_time, end_time)
            if actual_start < actual_end:
                events.append((actual_start, 1))
                events.append((actual_end, -1))

        events.sort(key=lambda x:(x[0], x[1]))

        max_simultaneous = 0
        current_active = 0

        for time_point, change in events:
            current_active += change
            if current_active > max_simultaneous:
                max_simultaneous = current_active

        if max_simultaneous >= item.quantity:
            print(f"Відмова {item.quantity} шт. '{item.name}' вже заброньовані")
            return False

        new_rental = Rental(client_id=client_id, equipment_id=equipment_id, start_time=start_time, end_time=end_time)
        self.db_session.add(new_rental)
        self.db_session.commit()
        print("Успішно орендовано")
        return True

    def return_equipment(self, client_id, rental_id):
        rental = self.db_session.query(Rental).filter_by(id=rental_id, client_id=client_id).first()

        self.db_session.delete(rental)
        self.db_session.commit()
        return True

    def get_user_rentals(self, client_id):
        return self.db_session.query(Rental, Equipment).join(Equipment, Rental.equipment_id == Equipment.id).filter(Rental.client_id == client_id).all()