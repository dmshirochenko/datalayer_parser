import json
import redis
from typing import Any, Dict

from src.config.config import settings


class RedisJSONClient:
    def __init__(self, db_settings: Dict[str, Any]):
        self.redis_client = redis.Redis(
            host=db_settings["redis_host"],
            port=db_settings["redis_port"],
            password=db_settings["redis_password"],
            db=db_settings["redis_db"],
            decode_responses=True,
        )

    def set_json(self, key: str, value: Dict[str, Any], ex=None) -> bool:
        """
        Serialize a dictionary to a JSON string and store it in Redis.
        """
        try:
            json_value = json.dumps(value)
            return self.redis_client.set(key, json_value, ex=ex)
        except redis.RedisError as e:
            print(f"Redis error: {e}")
            return False
        except TypeError as e:
            print(f"Serialization error: {e}")
            return False

    def get_json(self, key: str) -> Dict[str, Any]:
        """
        Retrieve a JSON string from Redis and deserialize it to a dictionary.
        """
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            else:
                return {}  # Key does not exist
        except redis.RedisError as e:
            print(f"Redis error: {e}")
            return {}
        except json.JSONDecodeError as e:
            print(f"Deserialization error: {e}")
            return {}


def get_redis_connection() -> RedisJSONClient:
    db_settings = {
        "redis_host": settings.redis_host,
        "redis_port": settings.redis_port,
        "redis_password": settings.redis_password,
        "redis_db": settings.redis_db,
    }
    return RedisJSONClient(db_settings=db_settings)
