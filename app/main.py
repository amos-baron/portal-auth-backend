import os, sys
import uvicorn
from settings import settings

APP_INTERFACE = settings.app_interface
APP_PORT = settings.app_port

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.routes import router as auth_router
from user_info.routes import router as user_info_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")
app.include_router(user_info_router, prefix="/user_info")

if __name__ == '__main__':
    uvicorn.run(app, host=APP_INTERFACE, port=APP_PORT)


