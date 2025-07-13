# app/dependencies.py
from fastapi import Depends, Query
from sqlalchemy.orm import Session
from .database import get_db

def pagination_params(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=500)
):
    offset = (page - 1) * limit
    return {"limit": limit, "offset": offset}

def get_pagination(p=Depends(pagination_params)):
    return p

# Em routers:
# items = db.query(...).offset(p["offset"]).limit(p["limit"]).all()