from equipment import Equipment

class EquipmentService:
    def __init__(self, db_session):
        self.db_session = db_session

    def add_equipment(self, name: str, category: str, price: int, quantity: int):
        if price <= 0:
            raise ValueError("Ціна оренди має бути більшою за нуль.")
        if quantity < 0:
            raise ValueError("Кількість не може бути від'ємною.")

        new_item = Equipment(
            name=name,
            category=category,
            price=price,
            quantity=quantity
        )

        self.db_session.add(new_item)
        self.db_session.commit()
        return new_item

    def get_all_equipment(self):
        return self.db_session.query(Equipment).all()

    def delete_equipment(self, equipment_id):
        item = self.db_session.query(Equipment).filter_by(id=equipment_id).first()
        if item:
            self.db_session.delete(item)
            self.db_session.commit()
            return True
        return False

    def update_equipment(self, equipment_id: int, new_price: int, new_quantity: int):
        item = self.db_session.query(Equipment).filter_by(id=equipment_id).first()
        if item:
            item.price = new_price
            item.quantity = new_quantity
            self.db_session.commit()
            return True
        return False
