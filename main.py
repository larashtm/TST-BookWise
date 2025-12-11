from fastapi import FastAPI
from fastapi.openapi.models import APIKey, APIKeyIn, SecuritySchemeType
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer
from api.loan_router import router as loan_router
from auth.auth_router import router as auth_router

app = FastAPI(title="BookWise - Lending BC (with Auth)")
bearer_scheme = HTTPBearer()

@app.get("/")
def root():
    return {"message": "BookWise API is running"}

# Register routers
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

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [
                {"BearerAuth": []}
            ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# Vercel serverless function handler
if __name__ != "__main__":
    # This is for Vercel
    handler = app
