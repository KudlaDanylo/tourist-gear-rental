from equipment import Equipment
from rental import Rental

class RentalService:
    def __init__(self,db_session):
        self.db_session = db_session

    def rent_equipment(self, client_id, equipment_id):
        item = self.db_session.query(Equipment).filter_by(id=equipment_id).first()

        if not item:
            print("Такого спорядження не існує")
            return  False
        if item.quantity <= 0:
            print("На жаль, '{item.name}' зараз немає в наявності")
            return False
        item.quantity -= 1

        new_rental = Rental(client_id=client_id, equipment_id=equipment_id)
        self.db_session.add(new_rental)
        self.db_session.commit()
        print("Успішно орендовано")
        return True

    def return_equipment(self, client_id, rental_id):
        rental = self.db_session.query(Rental).filter_by(id=rental_id, client_id=client_id).first()
        item = self.db_session.query(Equipment).filter_by(id=rental.equipment_id).first()
        if item:
            item.quantity += 1

        self.db_session.delete(rental)
        self.db_session.commit()
        return True

    def get_user_rentals(self, client_id):
        return self.db_session.query(Rental, Equipment).join(Equipment, Rental.equipment_id == Equipment.id).filter(Rental.client_id == client_id).all()