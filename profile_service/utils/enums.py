from enum import Enum


class ShardedCollections(Enum):
    # Закладки/избранные фильмы пользователей
    BOOKMARKS_COLLECTION = ("bookmarksCollection", {"user_id": "hashed", "movie_id": 1})

    # Рейтинги фильмов от пользователей
    RATINGS_COLLECTION = ("ratingsCollection", {"movie_id": "hashed", "user_id": 1})

    # Рецензии на фильмы
    REVIEWS_COLLECTION = ("reviewsCollection", {"movie_id": "hashed", "created_at": 1})

    def __init__(self, collection_name, shard_key):
        self.collection_name = collection_name
        self.shard_key = shard_key


class BookmarkType(str, Enum):
    """
    Тип закладок
    """
    FAVORITE = "favorite"
    WATCHLIST = "watchlist"