from fastapi import FastAPI, HTTPException, Query
from models import Ferrari, FerrariUpdate
import store

app = FastAPI(
    title="Ferrari Service",
    description="REST API for managing Ferrari car catalog",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ferraris", response_model=list[Ferrari])
def list_ferraris(
    year: int | None = Query(None, description="Filter by year"),
    engine: str | None = Query(None, description="Filter by engine type"),
):
    cars = store.get_all()
    if year is not None:
        cars = [c for c in cars if c.year == year]
    if engine is not None:
        cars = [c for c in cars if c.engine.value.lower() == engine.lower()]
    return cars


@app.get("/ferraris/{car_id}", response_model=Ferrari)
def get_ferrari(car_id: int):
    car = store.get(car_id)
    if car is None:
        raise HTTPException(status_code=404, detail=f"Ferrari {car_id} not found")
    return car


@app.post("/ferraris", response_model=Ferrari, status_code=201)
def create_ferrari(car: Ferrari):
    return store.create(car)


@app.patch("/ferraris/{car_id}", response_model=Ferrari)
def update_ferrari(car_id: int, data: FerrariUpdate):
    updates = data.model_dump(exclude_unset=True)
    car = store.update(car_id, updates)
    if car is None:
        raise HTTPException(status_code=404, detail=f"Ferrari {car_id} not found")
    return car


@app.delete("/ferraris/{car_id}", status_code=204)
def delete_ferrari(car_id: int):
    if not store.delete(car_id):
        raise HTTPException(status_code=404, detail=f"Ferrari {car_id} not found")
