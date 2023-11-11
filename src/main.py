import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from db.database import create_tables
from router import router

app = FastAPI(title="Catalog-AI")

origins = ["127.0.0.1:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)


def main():
    asyncio.run(create_tables())
    app.include_router(router)
    uvicorn.run(app=app, host="127.0.0.1", port=8080)


if __name__ == "__main__":
    main()
