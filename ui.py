from validation import Validation
from auth_service import AuthService, SessionManager
from equipment_service import EquipmentService

class ConsoleUI:
    def __init__(self, auth_service: AuthService, session_manager: SessionManager, equipment_service: EquipmentService):
        self.auth_service = auth_service
        self.session_manager = session_manager
        self.equipment_service = equipment_service

    def run(self):
        is_running = True
        while is_running:
            if self.session_manager.is_authenticated():
                is_running = self._show_user_menu()
            else:
                is_running = self._show_quest_menu()


    def _show_quest_menu(self):
        print("1. Реєстрація")
        print("2. Вхід")
        print("0. Вийти")

        choice = input("Оберіть дію: ")

        if choice == "1":
            self._handle_registration()
        elif choice == "2":
            self._handle_login()
        elif choice == "0":
            print("Завершення роботи...")
            return False
        else:
            print("Невідома команда")
        return True

    def _show_user_menu(self):
        current_user = self.session_manager.current_user
        print(f"Активний користувач: {current_user.name}")
        if current_user.admin:
            print("--- ПАНЕЛЬ АДМІНІСТРАТОРА ---")
            print("4. Додати нове спорядження")
            print("5. Змінити дані спорядження")
            print("6. Видалити спорядження")

        print("1. Доступне спорядження")
        print("2. Редагувати свій профіль")
        print("3. Вийти з акаунту")
        print("7. Видалити свій профіль (назавжди)")

        choice = input("Оберіть дію: ")
        if choice == "1":
            self._show_all_equipment()
        if choice == "2":
            self._handle_edit_profile()
        if choice == "3":
            self.auth_service.logout()
            print("Ви вийшли з системи")
        elif choice == "4" and current_user.admin:
            self._handle_add_equipment()
        elif choice == "5" and current_user.admin:
            self._handle_update_equipment()
        elif choice == "6" and current_user.admin:
            self._handle_delete_equipment()
        elif choice == "7":
            self._handle_delete_account()
        else:
            print("невідома команда")
        return True

    def _handle_registration(self):
        print("---Реєстрація---")
        name = input("Ім'я: ")
        age = input("Вік: ")
        number = input("Телефон: ")
        email = input("Email: ")
        password = input("Пароль: ")

        validation = Validation(name, age, number, email, password)
        errors = validation.run_all_audits()
        if errors:
            print("Виявлено помилки у введених даних")
            for field, error_message in errors.items():
                print(f" - {field.capitalize()}: {error_message}")
            return
        else:
            self.auth_service.register(name, age, number, email, password)
            print("Реєстрація успішна! Тепер ви можете увійти.")

    def _handle_login(self):
        print("\n--- ВХІД ---")
        email = input("Email: ")
        password = input("Пароль: ")

        try:
            self.auth_service.login(email, password)
            print(f"Вітаємо, {self.session_manager.current_user.name}!")
        except ValueError as e:
            print(f"Помилка: {e}")

    def _handle_add_equipment(self):
        print("Додавання нового спорядження")
        name = input("Назва товару: ")
        category = input("Категорія: ")
        price = int(input("Ціна за годину: "))
        quantity = int(input("Кількість на складі: "))
        self.equipment_service.add_equipment(name, category, price, quantity)
        print(f"Товар '{name}' у кількості {quantity} шт. успішно додано до бази!")

    def _show_all_equipment(self):
        items = self.equipment_service.get_all_equipment()
        if not items:
            print("Склад порожній")
            return
        print("ДОСТУПНЕ СПОРЯДЖЕННЯ")
        for item in items:
            print(f"[ID: {item.id}] {item.name} ({item.category}) | Ціна: {item.price} грн | Залишок: {item.quantity} шт.")
        input("Натисніть Enter, щоб повернутися до меню...")
        return True

    def _handle_delete_equipment(self):
        if not self._show_all_equipment():
            return

        item_id = int(input("Введіть ID товару який хочете видалити: "))
        if self.equipment_service.delete_equipment(item_id):
            print("Товар видалено")
        else:
            print("Товар не знайдено")

    def _handle_update_equipment(self):
        if not self._show_all_equipment():
            return
        item_id = int(input("Введіть ID для редагування: "))
        new_price = int(input("Нова ціна за добу: "))
        new_quantity = int(input("Нова кількість на складі: "))
        if self.equipment_service.update_equipment(item_id, new_price, new_quantity):
            print("Дані успішно оновлено!")
        else:
            print("Помилка: Товар з таким ID не знайдено.")

    def _handle_edit_profile(self):
        current_user = self.session_manager.current_user

        print("РЕДАГУВАННЯ ПРОФІЛЮ")
        new_name = input(f"Нове ім'я ({current_user.name}): ").strip()
        new_email = input(f"Нова пошта ({current_user.email}): ").strip()
        new_password = input("Новий пароль: ").strip()
        success = self.auth_service.update_user_data(
            user_id=current_user.id,
            new_name=new_name if new_name else None,
            new_email=new_email if new_email else None,
            new_password=new_password if new_password else None
        )
        if success:
            print("Ваші дані успішно оновлено!")
        else:
            print("Помилка: Не вдалося оновити профіль.")

    def _handle_delete_account(self):
        confirm = input("Ви впевнені? (напишіть 'так' для підтвердження): ").strip().lower()
        if confirm == 'так':
            current_user = self.session_manager.current_user
            if self.auth_service.delete_user(current_user.id):
                print("Ваш акаунт успішно видалено")
                self.session_manager.clear_session()
            else:
                print("Акаунт не знайдено")
        else:
            print("Видалення скасовано.")