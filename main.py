import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer
from api.loan_router import router as loan_router
from auth.auth_router import router as auth_router

app = FastAPI(title="BookWise - Lending BC (with Auth)")
bearer_scheme = HTTPBearer()

@app.get("/")
def root():
    return {"message": "BookWise API is running"}

app.include_router(auth_router)
app.include_router(loan_router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="BookWise - Lending BC (with Auth)",
        version="1.0.0",
        routes=app.routes,
    )

    openapi_schema.setdefault("components", {})
    openapi_schema["components"].setdefault("securitySchemes", {})
    openapi_schema["components"]["securitySchemes"]["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }

    for path, path_item in openapi_schema["paths"].items():
        for method, details in path_item.items():
            if method in ["get", "post", "put", "patch", "delete"]:
                details.setdefault("security", [{"BearerAuth": []}])

    app.openapi_schema = openapi_schema
    return openapi_schema

app.openapi = custom_openapi

# Vercel handler
handler = app