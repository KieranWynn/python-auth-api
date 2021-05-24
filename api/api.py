from fastapi import FastAPI

from typing import Dict

app = FastAPI()

@app.get("/", tags=["root"])
async def read_root() -> Dict[str, str]:
    return {"message": "Hello, World!"}
