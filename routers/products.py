from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database import get_db
from models.models import ProductModel, CategoryModel
from schemas.schemas import ProductCreate, ProductUpdate, StandardResponse

router = APIRouter(prefix="/products", tags=["Products"])

def format_resp(code: int, msg: str, data: any = None, err: str = None):
    return StandardResponse(statusCode=code, error=err, message=msg, data=data)
@router.get("/", response_model=StandardResponse)
def get_products(category_id: int = Query(None), search: str = Query(None), db: Session = Depends(get_db)):
    query = db.query(ProductModel)
    if category_id:
        query = query.filter(ProductModel.category_id == category_id)
    if search:
        query = query.filter(or_(ProductModel.name.ilike(f"%{search}%"), ProductModel.product_code.ilike(f"%{search}%")))
    
    return format_resp(200, "Lấy danh sách sản phẩm thành công", query.all())

@router.post("/", response_model=StandardResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    if db.query(ProductModel).filter(ProductModel.product_code == product.product_code).first():
        raise HTTPException(status_code=400, detail="Mã sản phẩm đã tồn tại")
    if not db.query(CategoryModel).filter(CategoryModel.id == product.category_id).first():
        raise HTTPException(status_code=404, detail="Danh mục không tồn tại")
        
    new_prod = ProductModel(**product.model_dump())
    db.add(new_prod)
    db.commit()
    db.refresh(new_prod)
    return format_resp(201, "Thêm sản phẩm thành công", new_prod)

@router.put("/{id}", response_model=StandardResponse)
def update_product(id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    prod = db.query(ProductModel).filter(ProductModel.id == id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Sản phẩm không tồn tại")
    if product_update.price is not None:
        prod.price = product_update.price
    if product_update.stock_quantity is not None:
        prod.stock_quantity = product_update.stock_quantity
    db.commit()
    db.refresh(prod)
    return format_resp(200, "Cập nhật sản phẩm thành công", prod)