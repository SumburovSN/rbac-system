from app.api.schemas.goods import GoodCreate, Good, GoodUpdate


class MockGoodsRepository:
    def __init__(self):
        self.goods = []
        self.last_id = 0
        self.seed()

    def seed(self):
        initial_goods = [
            {"name": "Laptop", "price": 1200.99},
            {"name": "Smartphone", "price": 899.50},
            {"name": "Headphones", "price": 150.00},
            {"name": "Monitor", "price": 300.00},
            {"name": "Keyboard", "price": 75.00},
            {"name": "Mouse", "price": 45.00},
            {"name": "USB Flash 64GB", "price": 20.00},
            {"name": "External HDD 1TB", "price": 85.00},
            {"name": "Webcam", "price": 55.00},
            {"name": "Microphone", "price": 110.00},
        ]

        for item in initial_goods:
            self.create(GoodCreate(**item))

    def get_all(self):
        return self.goods

    def get_by_id(self, good_id: int):
        for item in self.goods:
            if item.id == good_id:
                return item
        return None

    def create(self, item: GoodCreate):
        self.last_id += 1
        new_item = Good(id=self.last_id, **item.model_dump())
        self.goods.append(new_item)
        return new_item

    def update(self, good_id: int, update_data: GoodUpdate):
        item = self.get_by_id(good_id)
        if not item:
            return None

        if update_data.name is not None:
            item.name = update_data.name

        if update_data.price is not None:
            item.price = update_data.price

        return item

    def delete(self, good_id: int):
        item = self.get_by_id(good_id)
        if not item:
            return False

        self.goods.remove(item)
        return True
