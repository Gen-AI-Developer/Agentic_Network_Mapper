from fastapi import FastAPI
app = FastAPI(title="Agentic Network Mapper", version="0.1.0")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Agentic Network Mapper API!"}

