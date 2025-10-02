from typing import List
from kluster.models import User, CollectionItem

class SearchService:
    @staticmethod
    def search_users(term: str) -> List[User]:
        like = f"%{term}%"
        return User.query.filter(User.username.ilike(like)).limit(20).all()

    @staticmethod
    def search_items(term: str) -> List[CollectionItem]:
        like = f"%{term}%"
        return CollectionItem.query.filter(CollectionItem.name.ilike(like)).limit(20).all()
