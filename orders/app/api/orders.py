import time 
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from app.database import get_async_session
from app.api.models import order
from app.api.schemas import OrderCreate


router = APIRouter(
    prefix ="/orders",
    tags = ['Order']
)

@router.get('/long_order')
@cache(expire=60)
def get_long_op():
    time.sleep(2)
    return 'Много данных'

@router.get('/{order_id}')
async def get_specific_orders(order_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(order).where(order.c.order_id == order_id)
        result = await session.execute(query)
        order_data = result.fetchone()
        
        if order_data:
            order_dict = dict(order_data._asdict())
            return order_dict
        else:
            return None
    except Exception:
        raise HTTPException(status_code= 500, detail={
            'status': 'error',
            'data': None,
            'details': None,
        })
    

@router.post('/')
async def add_specific_orders(new_order: OrderCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        query = insert(order).values(**new_order.dict())
        await session.execute(query)
        await session.commit()
        return {'status': 'success'}
    except Exception:
        raise HTTPException(status_code= 500, detail={
            'status': 'error',
            'data': None,
            'details': None,
        })


