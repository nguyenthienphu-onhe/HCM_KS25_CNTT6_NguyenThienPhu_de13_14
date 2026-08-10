from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.models import CategoryModel, ProductModel
from schemas.schemas import StandardResponse

router = APIRouter(prefix="/categories", tags=["Categories"])

def format_resp(code: int, msg: str, data: any = None, err: str = None):
    return StandardResponse(statusCode=code, error=err, message=msg, data=data)

@router.delete("/{id}", response_model=StandardResponse)
def delete_category(id: int, db: Session = Depends(get_db)):
    category = db.query(CategoryModel).filter(CategoryModel.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Danh mục không tồn tại")
    products_count = db.query(ProductModel).filter(ProductModel.category_id == id).count()
    if products_count > 0:
        raise HTTPException(status_code=400, detail="Không thể xóa danh mục đang chứa sản phẩm")
        
    db.delete(category)
    db.commit()
    return format_resp(200, "Xóa danh mục thành công")