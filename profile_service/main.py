from fastapi import FastAPI
from profile_service.routs import router


app = FastAPI()
app.include_router(router)
