from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.auth.views import auth_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]

)

@app.get('/')
def get_main():
    return {"messages":"welcome to the main page"}

@app.get('/healthcheck')
def healthcheck():
    return {"messages":"This route is for health-check"}


app.include_router(auth_router)

