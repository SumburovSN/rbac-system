from app.api.schemas.orders import Order, OrderCreate, OrderUpdate


class MockOrdersRepository:
    def __init__(self):
        self.orders = []
        self.last_id = 0
        self.seed()

    def seed(self):
        initial_orders = [
            {
                "id": 1,
                "manufacturer": "Acme Corp",
                "description": "Поставка экспериментальных прототипов серии X."
            },
            {
                "id": 2,
                "manufacturer": "Nordic Steel",
                "description": "Заказ на изготовление стальных компонентов для промышленного оборудования."
            },
            {
                "id": 3,
                "manufacturer": "Sunrise Electronics",
                "description": "Поставка микросхем для партии тестовых устройств."
            },
            {
                "id": 4,
                "manufacturer": "GreenField Agro",
                "description": "Закупка оборудования для агротехнических исследований."
            },
            {
                "id": 5,
                "manufacturer": "AeroDynamics Lab",
                "description": "Изготовление деталей для экспериментального беспилотника."
            },
            {
                "id": 6,
                "manufacturer": "QuantumTech",
                "description": "Тестовая партия квантовых сенсоров."
            },
            {
                "id": 7,
                "manufacturer": "BlueOcean Robotics",
                "description": "Производство корпусов для подводных роботов."
            }
        ]

        for order in initial_orders:
            self.create(OrderCreate(**order))

    def get_all(self):
        return self.orders

    def get_by_id(self, order_id: int):
        for order in self.orders:
            if order.id == order_id:
                return order
        return None

    def create(self, order: OrderCreate):
        self.last_id += 1
        new_order = Order(id=self.last_id, **order.model_dump())
        self.orders.append(new_order)
        return new_order

    def update(self, order_id: int, update_data: OrderUpdate):
        order = self.get_by_id(order_id)
        if not order:
            return None

        if update_data.manufacturer is not None:
            order.manufacturer = update_data.manufacturer

        if update_data.description is not None:
            order.description = update_data.description

        return order

    def delete(self, order_id: int):
        order = self.get_by_id(order_id)
        if not order:
            return False

        self.orders.remove(order)
        return True
