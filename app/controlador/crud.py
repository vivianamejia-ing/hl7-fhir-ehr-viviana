from sqlalchemy.orm import Session
from modelo.models import Item
from modelo.schemas import ItemCreateOrUpdate
from datetime import datetime

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def get_items(db: Session, limit: int = 100):
    return db.query(Item).limit(limit).all()

def create_item(db: Session, item: ItemCreateOrUpdate):
    db_item = Item(**item.dict())
    db_item.dateOfCreation = datetime.utcnow()
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        return None
    db.delete(db_item)
    db.commit()
    return db_item

def update_item(db: Session, item: ItemCreateOrUpdate, item_id: int):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        return None
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item