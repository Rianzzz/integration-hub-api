import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from integration_hub.api.routers import auth, customers, health
from integration_hub.core.logging import configure_logging
from integration_hub.domain.exceptions import CustomerNotFoundError, InvalidCredentialsError

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(title="Integration Hub API")

    @app.exception_handler(CustomerNotFoundError)
    def handle_customer_not_found(_request: Request, exc: CustomerNotFoundError) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(InvalidCredentialsError)
    def handle_invalid_credentials(_request: Request, exc: InvalidCredentialsError) -> JSONResponse:
        return JSONResponse(
            status_code=401,
            content={"detail": str(exc)},
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(Exception)
    def handle_unexpected_error(_request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Erro nao tratado: %s", exc)
        return JSONResponse(status_code=500, content={"detail": "Erro interno inesperado"})

    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(customers.router)
    return app


app = create_app()
