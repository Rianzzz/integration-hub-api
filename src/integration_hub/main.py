from fastapi import FastAPI

from integration_hub.api.routers import customers, health


def create_app() -> FastAPI:
    app = FastAPI(title="Integration Hub API")
    app.include_router(health.router)
    app.include_router(customers.router)
    return app


app = create_app()
