from fastapi import FastAPI
from analyser.routes import router as analyser_router
app = FastAPI()
app.include_router(analyser_router)
