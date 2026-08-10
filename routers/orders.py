from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.models import OrderModel, OrderItemModel, ProductModel
from schemas.schemas import OrderCreate, StandardResponse
import time

router = APIRouter(prefix="/orders", tags=["Orders"])

def format_resp(code: int, msg: str, data: any = None, err: str = None):
    return StandardResponse(statusCode=code, error=err, message=msg, data=data)

@router.post("/", response_model=StandardResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    order_code = f"ORD{int(time.time())}"
    new_order = OrderModel(order_code=order_code, customer_name=order.customer_name, status="COMPLETED")
    db.add(new_order)
    db.flush()
    total_amount = 0.0
    for item in order.items:
        prod = db.query(ProductModel).filter(ProductModel.id == item.product_id).first()
        if not prod:
            db.rollback()
            raise HTTPException(status_code=404, detail=f"Sản phẩm ID {item.product_id} không tồn tại")
        if prod.stock_quantity < item.quantity:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Sản phẩm {prod.name} không đủ tồn kho")
            
        prod.stock_quantity -= item.quantity
        order_item = OrderItemModel(
            order_id=new_order.id,
            product_id=prod.id,
            quantity=item.quantity,
            unit_price=prod.price
        )
        db.add(order_item)
        total_amount += (prod.price * item.quantity)
        
    new_order.total_amount = total_amount
    db.commit()
    db.refresh(new_order)
    return format_resp(201, "Tạo đơn hàng thành công", new_order)

@router.get("/{id}", response_model=StandardResponse)
def get_order_details(id: int, db: Session = Depends(get_db)):
    order = db.query(OrderModel).filter(OrderModel.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Đơn hàng không tồn tại")
    return format_resp(200, "Lấy chi tiết đơn hàng thành công", order)