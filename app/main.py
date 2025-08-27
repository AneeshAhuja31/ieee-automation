from fastapi import FastAPI

app = FastAPI()

@app.get("/fetch-instagram")
async def fetch_instagram():
    pass