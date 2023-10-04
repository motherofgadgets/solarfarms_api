from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the Solar Farms Application!"}


@app.get("/farms/{farm_id}")
async def farms(farm_id: int):
    return {"farm": farm_id}
