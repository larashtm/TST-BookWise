from fastapi import FastAPI
from api.loan_router import router as loan_router
from auth.auth_router import router as auth_router

app = FastAPI(title="BookWise - Lending BC (with Auth)")

@app.get("/")
def root():
    return {"message": "BookWise API is running"}

# register auth router first
app.include_router(auth_router)
# register loan router
app.include_router(loan_router)
