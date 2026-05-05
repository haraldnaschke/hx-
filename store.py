from models import Ferrari, EngineType

_next_id = 1
_db: dict[int, Ferrari] = {}


def _seed():
    global _next_id
    seeds = [
        Ferrari(model="SF90 Stradale", year=2023, engine=EngineType.hybrid,
                horsepower=986, top_speed_kmh=340, price_usd=507000),
        Ferrari(model="F8 Tributo", year=2022, engine=EngineType.v8,
                horsepower=710, top_speed_kmh=340, price_usd=276000),
        Ferrari(model="812 Superfast", year=2021, engine=EngineType.v12,
                horsepower=789, top_speed_kmh=340, price_usd=335000),
        Ferrari(model="Roma", year=2023, engine=EngineType.v8,
                horsepower=612, top_speed_kmh=320, price_usd=222000),
    ]
    for car in seeds:
        create(car)


def get_all() -> list[Ferrari]:
    return list(_db.values())


def get(car_id: int) -> Ferrari | None:
    return _db.get(car_id)


def create(car: Ferrari) -> Ferrari:
    global _next_id
    car = car.model_copy(update={"id": _next_id})
    _db[_next_id] = car
    _next_id += 1
    return car


def update(car_id: int, data: dict) -> Ferrari | None:
    car = _db.get(car_id)
    if car is None:
        return None
    updated = car.model_copy(update=data)
    _db[car_id] = updated
    return updated


def delete(car_id: int) -> bool:
    if car_id not in _db:
        return False
    del _db[car_id]
    return True


_seed()
