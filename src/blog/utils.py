import os

import redis

# إعداد الاتصال بـ Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))


redis_client = redis.StrictRedis(
    host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True
)

BLACKLIST_KEY = "jwt_blacklist"


def add_token_to_blacklist(token: str):
    """
    تضيف التوكن للـ blacklist في Redis
    """
    # Optional: ممكن تضيف expiry لو التوكن له مدة صلاحية
    redis_client.sadd(BLACKLIST_KEY, token)


def is_token_blacklisted(token: str) -> bool:
    """
    تشيك إذا التوكن موجود في blacklist
    """
    return redis_client.sismember(BLACKLIST_KEY, token)
