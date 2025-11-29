from fastapi import FastAPI
from api.loan_router import router as loan_router
from api.loan_router import router as auth_router

app = FastAPI()

@app.get("/")
def root():
    return{"message": "BookWise API is running"}
app.include_router(loan_router)
app.include_router(auth_router)
