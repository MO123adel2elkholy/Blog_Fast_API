from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

redis_path = "redis://localhost:6379"

limiter = Limiter(key_func=get_remote_address, storage_uri=redis_path)
