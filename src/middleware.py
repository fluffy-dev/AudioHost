from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def init_middleware(app: FastAPI):
    origins = [
        "http://localhost:3000",  # React/Angular/Vue development
        "https://www.example.com",  # Production frontend
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )