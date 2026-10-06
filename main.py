from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from database import engine, Base
from routers import products, orders

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ecommerce Management API"
)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "statusCode": exc.status_code,
            "error": "Lỗi hệ thống hoặc Logic",
            "message": str(exc.detail),
            "data": None
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "statusCode": 400,
            "error": "Validation Error",
            "message": "Dữ liệu truyền lên không hợp lệ",
            "data": exc.errors()
        }
    )

app.include_router(categories.router)
app.include_router(products.router)
app.include_router(orders.router)
