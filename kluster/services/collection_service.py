from typing import List, Optional
from statistics import fmean
from kluster.models import db, CollectionItem
import structlog

log = structlog.get_logger()

class CollectionService:
    @staticmethod
    def add_item(user_id: int, name: str, description: str, category: str, estimated_value: float) -> CollectionItem:
        item = CollectionItem(user_id=user_id, name=name, description=description, category=category, estimated_value=estimated_value)
        db.session.add(item)
        db.session.commit()
        log.info("collection_item_added", user_id=user_id, item_id=item.id)
        return item

    @staticmethod
    def list_items(user_id: int) -> List[CollectionItem]:
        return CollectionItem.query.filter_by(user_id=user_id).order_by(CollectionItem.created_at.desc()).all()

    @staticmethod
    def total_value(user_id: int) -> float:
        values = [i.estimated_value for i in CollectionService.list_items(user_id)]
        return float(sum(values))

    @staticmethod
    def average_value(user_id: int) -> float:
        values = [i.estimated_value for i in CollectionService.list_items(user_id)]
        return float(fmean(values)) if values else 0.0

    @staticmethod
    def find_item(user_id: int, item_id: int) -> Optional[CollectionItem]:
        return CollectionItem.query.filter_by(user_id=user_id, id=item_id).first()

    @staticmethod
    def delete_item(user_id: int, item_id: int) -> None:
        item = CollectionService.find_item(user_id, item_id)
        if not item:
            raise ValueError("Item not found")
        db.session.delete(item)
        db.session.commit()
        log.info("collection_item_deleted", user_id=user_id, item_id=item_id)
